"""External provider clients for trigger monitoring."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from accounts.core.config import settings


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=2,
        read=2,
        connect=2,
        backoff_factor=0.6,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "RakshakTriggerMonitor/1.0"})
    return session


def _get_json(url: str, *, params: dict[str, Any], timeout: int = 15) -> dict[str, Any]:
    session = _build_session()
    response = session.get(
        url,
        params=params,
        timeout=timeout,
        verify=settings.external_requests_verify_ssl,
    )
    response.raise_for_status()
    return response.json()


def fetch_weather_snapshot(*, lat: float, lon: float) -> dict[str, Any]:
    payload = _get_json(
        settings.weather_base_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation,temperature_2m",
            "forecast_days": 2,
            "past_days": 1,
            "timezone": "UTC",
        },
        timeout=15,
    )
    hourly = payload.get("hourly", {})
    timestamps = hourly.get("time", [])
    precipitation = hourly.get("precipitation", [])
    temperature = hourly.get("temperature_2m", [])
    now = datetime.now(timezone.utc)
    recent_values: list[float] = []
    recent_temps: list[float] = []
    for ts_raw, rain_value, temp_value in zip(timestamps, precipitation, temperature):
        ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
        if now - timedelta(hours=2) <= ts <= now + timedelta(hours=1):
            recent_values.append(float(rain_value or 0))
            recent_temps.append(float(temp_value or 0))
    observed = max(recent_values) if recent_values else 0.0
    avg_temp = sum(recent_temps) / len(recent_temps) if recent_temps else 0.0
    return {
        "observed_value": observed,
        "average_temperature": round(avg_temp, 2),
        "raw": payload,
    }


def fetch_aqi_snapshot(*, lat: float, lon: float) -> dict[str, Any]:
    if settings.waqi_api_token:
        payload = _get_json(
            f"{settings.waqi_base_url}:{lat};{lon}/",
            params={"token": settings.waqi_api_token},
            timeout=15,
        )
        if payload.get("status") == "ok":
            aqi_value = float(payload.get("data", {}).get("aqi", 0))
            return {"observed_value": aqi_value, "source": "waqi", "raw": payload}

    if settings.aqi_fallback_source == "openmeteo":
        payload = _get_json(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "us_aqi",
                "forecast_days": 2,
                "past_days": 1,
                "timezone": "UTC",
            },
            timeout=15,
        )
        values = [float(item or 0) for item in payload.get("hourly", {}).get("us_aqi", [])]
        observed = max(values[-3:]) if values else 0.0
        return {"observed_value": observed, "source": "openmeteo", "raw": payload}

    raise RuntimeError("No AQI provider is configured")


def fetch_news_snapshot(*, location_name: str) -> dict[str, Any]:
    if not settings.news_api_key:
        return {"observed_value": 0.0, "keywords": [], "articles": []}

    payload = _get_json(
        settings.news_api_base_url,
        params={
            "apiKey": settings.news_api_key,
            "q": f"({settings.news_query}) AND {location_name}",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
        },
        timeout=15,
    )
    keywords = ("bandh", "strike", "curfew")
    scored_articles = []
    for article in payload.get("articles", []):
        haystack = " ".join(
            [
                article.get("title", ""),
                article.get("description", ""),
                article.get("content", ""),
            ]
        ).lower()
        matches = [keyword for keyword in keywords if keyword in haystack]
        if not matches:
            continue
        confidence = min(1.0, 0.35 + 0.25 * len(matches))
        scored_articles.append(
            {
                "title": article.get("title"),
                "url": article.get("url"),
                "keywords": matches,
                "confidence": round(confidence, 2),
            }
        )
    observed = max((item["confidence"] for item in scored_articles), default=0.0)
    return {"observed_value": observed, "keywords": keywords, "articles": scored_articles}
