"""AQI feature service using WAQI with a real-data fallback."""

from __future__ import annotations

from typing import Any

import requests

from utils.config_loader import settings


def get_aqi_features(lat: float, lon: float) -> dict[str, float | str]:
    if settings.WAQI_API_TOKEN:
        response = requests.get(
            f"{settings.WAQI_BASE_URL}:{lat};{lon}/",
            params={"token": settings.WAQI_API_TOKEN},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") == "ok":
            aqi_value = float(payload.get("data", {}).get("aqi", 0))
            return {
                "current_aqi": aqi_value,
                "aqi_trend": round(min(1.0, aqi_value / 500.0), 3),
                "aqi_source": "waqi",
            }

    if settings.AQI_FALLBACK_SOURCE == "openmeteo":
        response = requests.get(
            settings.AQI_FALLBACK_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "us_aqi",
                "forecast_days": 2,
                "past_days": 1,
                "timezone": "UTC",
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        values = [float(item or 0) for item in payload.get("hourly", {}).get("us_aqi", [])]
        current_aqi = values[-1] if values else 0.0
        trailing = values[-6:] if len(values) >= 6 else values
        trend = sum(trailing) / len(trailing) if trailing else current_aqi
        return {
            "current_aqi": round(current_aqi, 2),
            "aqi_trend": round(min(1.0, trend / 500.0), 3),
            "aqi_source": "openmeteo",
        }

    raise RuntimeError("No AQI provider is configured")
