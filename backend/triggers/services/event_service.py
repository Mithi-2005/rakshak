"""Trigger evaluation and persistence helpers."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from accounts.core.config import settings
from policies.models import Policy, PolicyStatus
from triggers.models import TriggerEvent, TriggerType
from triggers.services.location import get_location_for_pincode
from triggers.services.providers import (
    fetch_aqi_snapshot,
    fetch_news_snapshot,
    fetch_weather_snapshot,
)

logger = logging.getLogger(__name__)


def get_active_pincodes(db: Session) -> list[str]:
    today = datetime.now(timezone.utc).date()
    rows = db.scalars(
        select(Policy.pincode)
        .where(Policy.status == PolicyStatus.ACTIVE)
        .where(Policy.end_date >= today)
        .distinct()
    )
    return list(rows)


def _upsert_trigger_event(
    *,
    pincode: str,
    trigger_type: TriggerType,
    observed_value: float,
    threshold_value: float,
    severity: float,
    source_payload: dict,
    db: Session,
) -> None:
    now = datetime.now(timezone.utc)
    existing = db.scalar(
        select(TriggerEvent)
        .where(TriggerEvent.pincode == pincode)
        .where(TriggerEvent.trigger_type == trigger_type)
        .where(TriggerEvent.end_time.is_(None))
    )
    if existing is not None:
        existing.observed_value = observed_value
        existing.severity = max(existing.severity, severity)
        existing.source_payload = source_payload
        return

    db.add(
        TriggerEvent(
            pincode=pincode,
            trigger_type=trigger_type,
            severity=severity,
            threshold_value=threshold_value,
            observed_value=observed_value,
            source_payload=source_payload,
            start_time=now,
            end_time=None,
            created_at=now,
            is_processed=False,
        )
    )


def _close_trigger_if_open(*, pincode: str, trigger_type: TriggerType, db: Session) -> None:
    existing = db.scalar(
        select(TriggerEvent)
        .where(TriggerEvent.pincode == pincode)
        .where(TriggerEvent.trigger_type == trigger_type)
        .where(TriggerEvent.end_time.is_(None))
    )
    if existing is not None:
        existing.end_time = datetime.now(timezone.utc)


def poll_all_active_zones(db: Session) -> dict[str, int]:
    created_or_updated = 0
    closed = 0
    provider_errors = 0
    for pincode in get_active_pincodes(db):
        location = get_location_for_pincode(pincode)

        try:
            weather = fetch_weather_snapshot(lat=location["lat"], lon=location["lon"])
            rain_value = float(weather["observed_value"])
            rain_severity = min(1.0, rain_value / max(settings.rain_trigger_threshold, 0.1))
            if rain_value > settings.rain_trigger_threshold:
                _upsert_trigger_event(
                    pincode=pincode,
                    trigger_type=TriggerType.RAIN,
                    observed_value=rain_value,
                    threshold_value=settings.rain_trigger_threshold,
                    severity=round(rain_severity, 2),
                    source_payload=weather,
                    db=db,
                )
                created_or_updated += 1
            else:
                _close_trigger_if_open(
                    pincode=pincode, trigger_type=TriggerType.RAIN, db=db
                )
                closed += 1
        except Exception as exc:
            provider_errors += 1
            logger.warning(
                "Weather polling failed | pincode=%s | error=%s",
                pincode,
                exc,
            )

        try:
            aqi = fetch_aqi_snapshot(lat=location["lat"], lon=location["lon"])
            aqi_value = float(aqi["observed_value"])
            aqi_severity = min(1.0, aqi_value / max(settings.aqi_trigger_threshold, 1))
            if aqi_value > settings.aqi_trigger_threshold:
                _upsert_trigger_event(
                    pincode=pincode,
                    trigger_type=TriggerType.AQI,
                    observed_value=aqi_value,
                    threshold_value=float(settings.aqi_trigger_threshold),
                    severity=round(aqi_severity, 2),
                    source_payload=aqi,
                    db=db,
                )
                created_or_updated += 1
            else:
                _close_trigger_if_open(
                    pincode=pincode, trigger_type=TriggerType.AQI, db=db
                )
                closed += 1
        except Exception as exc:
            provider_errors += 1
            logger.warning(
                "AQI polling failed | pincode=%s | error=%s",
                pincode,
                exc,
            )

        try:
            news = fetch_news_snapshot(location_name=location["city"])
            news_value = float(news["observed_value"])
            if news_value >= settings.news_trigger_threshold:
                _upsert_trigger_event(
                    pincode=pincode,
                    trigger_type=TriggerType.NEWS,
                    observed_value=news_value,
                    threshold_value=settings.news_trigger_threshold,
                    severity=round(news_value, 2),
                    source_payload=news,
                    db=db,
                )
                created_or_updated += 1
            else:
                _close_trigger_if_open(
                    pincode=pincode, trigger_type=TriggerType.NEWS, db=db
                )
                closed += 1
        except Exception as exc:
            provider_errors += 1
            logger.warning(
                "News polling failed | pincode=%s | error=%s",
                pincode,
                exc,
            )

    logger.info(
        "Trigger polling complete | updated=%s | closed=%s | provider_errors=%s",
        created_or_updated,
        closed,
        provider_errors,
    )
    return {
        "updated": created_or_updated,
        "closed": closed,
        "provider_errors": provider_errors,
    }


def list_trigger_events(db: Session, pincode: str | None = None) -> list[TriggerEvent]:
    query = select(TriggerEvent).order_by(TriggerEvent.created_at.desc())
    if pincode:
        query = query.where(TriggerEvent.pincode == pincode)
    return list(db.scalars(query))


def count_open_triggers(db: Session, pincode: str) -> int:
    return int(
        db.scalar(
            select(func.count(TriggerEvent.id))
            .where(TriggerEvent.pincode == pincode)
            .where(TriggerEvent.end_time.is_(None))
        )
        or 0
    )
