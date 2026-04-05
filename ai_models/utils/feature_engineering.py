"""Feature engineering module for weather-aware risk prediction."""

from typing import Dict
import logging

logger = logging.getLogger(__name__)


def create_features(
    location_info: Dict,
    weather_features: Dict,
    aqi_features: Dict,
    claim_history: int,
    avg_income: float,
) -> Dict[str, float]:
    """
    Create feature vector for model prediction.

    Args:
        location_info: Dict with city, risk_zone, etc.
        weather_features: Dict with past/future weather signals.
        claim_history: Number of previous claims
        avg_income: Average annual income

    Returns:
        Dict with features for model prediction
    """
    try:
        risk_zone = float(location_info.get("risk_zone", 0.5))
        rainy_hours_next_48h = float(weather_features.get("rainy_hours_next_48h", 0))
        avg_rainfall_next_48h = float(
            weather_features.get("avg_rainfall_next_48h", 0.0)
        )
        rainy_hours_last_24h = float(weather_features.get("rainy_hours_last_24h", 0))
        avg_temperature_next_48h = float(
            weather_features.get("avg_temperature_next_48h", 0.0)
        )
        aqi_trend = float(aqi_features.get("aqi_trend", 0.0))

        disruption_score = (
            rainy_hours_next_48h * 0.4
            + avg_rainfall_next_48h * 0.3
            + rainy_hours_last_24h * 0.2
            + risk_zone * 0.05
            + aqi_trend * 10 * 0.05
        )

        features = {
            "risk_zone": max(0.0, min(1.0, risk_zone)),
            "rainy_hours_next_48h": max(0.0, min(48.0, rainy_hours_next_48h)),
            "avg_rainfall_next_48h": max(0.0, avg_rainfall_next_48h),
            "rainy_hours_last_24h": max(0.0, min(24.0, rainy_hours_last_24h)),
            "avg_temperature_next_48h": avg_temperature_next_48h,
            "aqi_trend": max(0.0, min(1.0, aqi_trend)),
            "claim_history": max(0.0, float(claim_history)),
            "avg_income": max(0.0, float(avg_income)),
            "disruption_score": round(disruption_score, 3),
        }

        # Validate features
        _validate_features(features)

        return features

    except Exception as e:
        logger.error(f"Error creating features: {e}")
        raise


def _validate_features(features: Dict[str, float]) -> None:
    """
    Validate feature ranges.

    Args:
        features: Feature dict to validate

    Raises:
        ValueError: If features are invalid
    """
    # Check for required features
    required_features = [
        "risk_zone",
        "rainy_hours_next_48h",
        "avg_rainfall_next_48h",
        "rainy_hours_last_24h",
        "avg_temperature_next_48h",
        "aqi_trend",
        "claim_history",
        "avg_income",
        "disruption_score",
    ]

    for feature in required_features:
        if feature not in features:
            raise ValueError(f"Missing required feature: {feature}")

    # Check for NaN or None values
    for key, value in features.items():
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            raise ValueError(f"Feature {key} has invalid value: {value}")

    # Check ranges
    if not (0 <= features["risk_zone"] <= 1):
        logger.warning(f"risk_zone out of range: {features['risk_zone']}")

    if features["avg_rainfall_next_48h"] < 0:
        logger.warning(
            f"avg_rainfall_next_48h is negative: {features['avg_rainfall_next_48h']}"
        )

    if features["rainy_hours_next_48h"] < 0:
        logger.warning(
            f"rainy_hours_next_48h is negative: {features['rainy_hours_next_48h']}"
        )

    if features["rainy_hours_last_24h"] < 0:
        logger.warning(
            f"rainy_hours_last_24h is negative: {features['rainy_hours_last_24h']}"
        )


def get_feature_importance() -> Dict[str, float]:
    """
    Get typical feature importance from trained model.
    Used for explanation and debugging.

    Returns:
        Dict mapping feature names to importance scores
    """
    return {
        "risk_zone": 0.18,
        "rainy_hours_next_48h": 0.24,
        "avg_rainfall_next_48h": 0.20,
        "rainy_hours_last_24h": 0.11,
        "avg_temperature_next_48h": 0.06,
        "aqi_trend": 0.12,
        "claim_history": 0.16,
        "avg_income": 0.08,
        "disruption_score": 0.18,
    }
