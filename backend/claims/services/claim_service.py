"""Claim creation and listing helpers."""

from __future__ import annotations

from datetime import date, datetime, time, timezone

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from accounts.core.config import settings
from accounts.models import UserProfile
from claims.models import Claim, ClaimStatus
from policies.models import Policy, PolicyStatus
from triggers.models import TriggerEvent, TriggerType


def list_user_claims(user_id: int, db: Session) -> list[Claim]:
    return list(
        db.scalars(
            select(Claim).where(Claim.user_id == user_id).order_by(Claim.created_at.desc())
        )
    )


def calculate_claim_amount(
    *,
    trigger_type: TriggerType,
    severity: float,
    avg_daily_income: float,
    coverage_amount: float,
) -> float:
    cap_map = {
        TriggerType.RAIN: settings.claim_cap_rain,
        TriggerType.AQI: settings.claim_cap_aqi,
        TriggerType.NEWS: settings.claim_cap_news,
    }
    income_component = avg_daily_income * min(max(severity, 0.1), 1.0)
    coverage_cap = coverage_amount * 0.01
    return round(min(cap_map[trigger_type], coverage_cap, income_component), 2)


def create_claims_for_unprocessed_triggers(
    db: Session, run_date: date | None = None
) -> int:
    now = datetime.now(timezone.utc)
    run_date = run_date or now.date()
    created_count = 0

    for event in db.scalars(select(TriggerEvent).where(TriggerEvent.end_time.is_(None))):
        event.end_time = now

    day_start = datetime.combine(run_date, time.min, tzinfo=timezone.utc)
    trigger_events = list(
        db.scalars(
            select(TriggerEvent)
            .where(TriggerEvent.is_processed.is_(False))
            .where(TriggerEvent.start_time >= day_start)
            .where(
                or_(
                    TriggerEvent.end_time.is_not(None),
                    TriggerEvent.start_time <= now,
                )
            )
        )
    )

    for event in trigger_events:
        policies = list(
            db.scalars(
                select(Policy)
                .where(Policy.pincode == event.pincode)
                .where(Policy.status == PolicyStatus.ACTIVE)
                .where(Policy.start_date <= event.start_time.date())
                .where(Policy.end_date >= event.start_time.date())
            )
        )
        for policy in policies:
            existing = db.scalar(
                select(Claim).where(
                    and_(
                        Claim.policy_id == policy.id,
                        Claim.trigger_event_id == event.id,
                    )
                )
            )
            if existing is not None:
                continue

            profile = db.scalar(
                select(UserProfile).where(UserProfile.user_id == policy.user_id)
            )
            claim = Claim(
                user_id=policy.user_id,
                policy_id=policy.id,
                trigger_event_id=event.id,
                claim_amount=calculate_claim_amount(
                    trigger_type=event.trigger_type,
                    severity=event.severity,
                    avg_daily_income=float(profile.avg_daily_income or 0),
                    coverage_amount=policy.coverage_amount,
                ),
                status=ClaimStatus.CREATED,
                created_at=now,
                updated_at=now,
            )
            db.add(claim)
            created_count += 1

        event.is_processed = True

    db.flush()
    return created_count

