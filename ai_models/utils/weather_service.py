"""Weather service for Open-Meteo hourly forecast features."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from utils.config_loader import settings

logger = logging.getLogger(__name__)


def get_weather_features(lat: float, lon: float) -> Dict[str, float | str]:
    """Fetch weather features from Open-Meteo without synthetic fallback."""
    features = _fetch_open_meteo_weather(lat, lon)
    features["weather_source"] = "api"
    return features


def _fetch_open_meteo_weather(lat: float, lon: float) -> Dict[str, float]:
    """Fetch hourly weather from Open-Meteo and compute past/future features."""
    try:
        url = settings.WEATHER_BASE_URL
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation,temperature_2m",
            "forecast_days": 7,
            "past_days": 2,
            "timezone": "UTC",
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        return _parse_open_meteo_response(data)

    except requests.RequestException as e:
        logger.warning(f"Open-Meteo request failed: {e}")
        raise
    except Exception as e:
        logger.warning(f"Error parsing Open-Meteo response: {e}")
        raise


def _parse_open_meteo_response(data: Dict) -> Dict[str, float]:
    """Parse Open-Meteo hourly payload into past and future rainfall signals."""
    hourly = data.get("hourly", {})
    time_points = hourly.get("time", [])
    precipitation = hourly.get("precipitation", [])
    temperature = hourly.get("temperature_2m", [])

    if (
        not time_points
        or not precipitation
        or not temperature
        or len(time_points) != len(precipitation)
        or len(time_points) != len(temperature)
    ):
        raise ValueError("Incomplete hourly data in Open-Meteo response")

    now = datetime.utcnow()
    next_48h_end = now + timedelta(hours=48)
    last_24h_start = now - timedelta(hours=24)

    future_precip: List[float] = []
    past_precip: List[float] = []
    future_temps: List[float] = []

    for ts_raw, rain_raw, temp_raw in zip(time_points, precipitation, temperature):
        ts = _safe_parse_timestamp(ts_raw)
        if ts is None:
            continue

        rain = _safe_to_float(rain_raw)
        temp = _safe_to_float(temp_raw)

        if now <= ts < next_48h_end:
            future_precip.append(rain)
            future_temps.append(temp)
        elif last_24h_start <= ts < now:
            past_precip.append(rain)

    if not future_precip:
        raise ValueError("No forecast points available for next 48h")

    if not past_precip:
        raise ValueError("No historical weather points available for last 24h")

    return {
        "avg_rainfall_next_48h": round(_avg(future_precip), 3),
        "rainy_hours_next_48h": _count_rainy_hours(future_precip),
        "max_rainfall_next_48h": round(max(future_precip), 3),
        "avg_rainfall_last_24h": round(_avg(past_precip), 3),
        "rainy_hours_last_24h": _count_rainy_hours(past_precip),
        "avg_temperature_next_48h": round(_avg(future_temps), 3),
    }


def _safe_parse_timestamp(value: str) -> datetime | None:
    """Parse Open-Meteo timestamp safely."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except (TypeError, ValueError):
        return None


def _safe_to_float(value: float | int | None) -> float:
    """Convert numeric values to float while guarding against missing fields."""
    try:
        if value is None:
            return 0.0
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0


def _avg(values: List[float]) -> float:
    """Compute average safely."""
    return sum(values) / len(values) if values else 0.0


def _count_rainy_hours(values: List[float], threshold: float = 0.1) -> int:
    """Count hours where rainfall exceeds threshold in mm."""
    return sum(1 for item in values if item > threshold)
