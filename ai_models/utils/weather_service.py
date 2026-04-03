"""Weather service for Open-Meteo hourly forecast features."""

import logging
import math
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from utils.config_loader import settings

logger = logging.getLogger(__name__)


def get_weather_features(lat: float, lon: float) -> Dict[str, float | str]:
    """Fetch weather features from Open-Meteo with robust fallback."""
    try:
        features = _fetch_open_meteo_weather(lat, lon)
        features["weather_source"] = "api"
        return features

    except Exception as e:
        logger.warning(f"Failed to fetch weather data: {e}. Using fallback simulation.")
        features = _fallback_weather_features(lat, lon)
        features["weather_source"] = "fallback"
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

    if not time_points or not precipitation or len(time_points) != len(precipitation):
        raise ValueError("Incomplete hourly data in Open-Meteo response")

    now = datetime.utcnow()
    next_48h_end = now + timedelta(hours=48)
    last_24h_start = now - timedelta(hours=24)

    future_precip: List[float] = []
    past_precip: List[float] = []

    for ts_raw, rain_raw in zip(time_points, precipitation):
        ts = _safe_parse_timestamp(ts_raw)
        if ts is None:
            continue

        rain = _safe_to_float(rain_raw)

        if now <= ts < next_48h_end:
            future_precip.append(rain)
        elif last_24h_start <= ts < now:
            past_precip.append(rain)

    if not future_precip:
        raise ValueError("No forecast points available for next 48h")

    # If past values are unavailable, approximate recent past from near-future trend.
    if not past_precip:
        past_precip = [round(value * 0.8, 2) for value in future_precip[:24]]

    return {
        "avg_rainfall_next_48h": round(_avg(future_precip), 3),
        "rainy_hours_next_48h": _count_rainy_hours(future_precip),
        "max_rainfall_next_48h": round(max(future_precip), 3),
        "avg_rainfall_last_24h": round(_avg(past_precip), 3),
        "rainy_hours_last_24h": _count_rainy_hours(past_precip),
    }


def _fallback_weather_features(lat: float, lon: float) -> Dict[str, float]:
    """Create deterministic fallback weather features when API data is unavailable."""
    now = datetime.utcnow()
    hour_seed = now.hour + now.timetuple().tm_yday
    lat_factor = abs(math.sin(math.radians(lat)))
    lon_factor = abs(math.cos(math.radians(lon)))

    future_avg = 1.2 + lat_factor * 2.1 + (hour_seed % 6) * 0.2
    past_avg = future_avg * (0.75 + lon_factor * 0.15)
    future_rainy_hours = int(min(48, max(4, round(future_avg * 6 + lon_factor * 10))))
    past_rainy_hours = int(min(24, max(2, round(past_avg * 4 + lat_factor * 5))))
    max_rain = future_avg * (1.8 + lat_factor * 0.4)

    return {
        "avg_rainfall_next_48h": round(future_avg, 3),
        "rainy_hours_next_48h": future_rainy_hours,
        "max_rainfall_next_48h": round(max_rain, 3),
        "avg_rainfall_last_24h": round(past_avg, 3),
        "rainy_hours_last_24h": past_rainy_hours,
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
