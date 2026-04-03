"""
Main FastAPI application for ML prediction service.
Provides POST /predict endpoint for risk scoring and plan generation.
"""

import logging
import pickle
import json
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator

from utils.config_loader import settings
from utils.pincode_mapper import get_location_info, validate_pincode
from utils.weather_service import get_weather_features
from utils.feature_engineering import create_features
from utils.plan_generator import generate_plans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Risk Score & Premium Planning Service",
    description="ML service for insurance risk assessment and pricing",
    version="1.0.0",
)

# Global model cache
_model_cache = None


# ==================== Pydantic Models ====================


class PredictionRequest(BaseModel):
    """Request schema for prediction."""

    pincode: str = Field(..., min_length=6, max_length=6, description="6-digit pincode")
    claim_history: int = Field(..., ge=0, description="Number of previous claims")
    avg_income: float = Field(..., gt=0, description="Average annual income in INR")

    @validator("pincode")
    def validate_pincode_field(cls, v):
        if not validate_pincode(v):
            raise ValueError("Invalid pincode format (must be 6 digits)")
        return v


class Plan(BaseModel):
    """Insurance plan details."""

    plan_id: str
    coverage: float = Field(..., description="Coverage amount in thousands")
    premium: float = Field(..., description="Monthly premium in INR")
    coverage_multiplier: Optional[float] = None
    price_multiplier: Optional[float] = None


class PredictionResponse(BaseModel):
    """Response schema for prediction."""

    risk_score: float = Field(..., ge=0, le=1, description="Risk score between 0 and 1")
    risk_level: str = Field(..., description="Risk level category")
    plans: list[Plan]
    location: Optional[Dict] = None
    reasoning: Optional[Dict] = None


# ==================== Helper Functions ====================


def load_model():
    """Load trained model from disk."""
    global _model_cache

    if _model_cache is not None:
        return _model_cache

    model_path = settings._resolve_path(settings.MODEL_PATH)

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")

    try:
        with open(model_path, "rb") as f:
            _model_cache = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        return _model_cache

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


def load_pricing_config() -> Dict:
    """Load pricing configuration, supporting local and backend sources."""
    if settings.CONFIG_SOURCE == "backend":
        return _load_config_from_backend()
    else:
        return _load_config_from_local()


def _load_config_from_local() -> Dict:
    """Load pricing config from local JSON file."""
    config_path = settings._resolve_path(settings.PRICING_CONFIG_PATH)

    if not config_path.exists():
        logger.error(f"Pricing config not found at {config_path}")
        raise FileNotFoundError(f"Pricing config not found at {config_path}")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logger.info(f"Loaded pricing config from {config_path}")
        return config

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in pricing config: {e}")
        raise


def _load_config_from_backend() -> Dict:
    """Load pricing config from backend API."""
    import requests

    try:
        response = requests.get(settings.BACKEND_CONFIG_URL, timeout=5)
        response.raise_for_status()
        config = response.json()
        logger.info(f"Loaded pricing config from {settings.BACKEND_CONFIG_URL}")
        return config

    except requests.RequestException as e:
        logger.error(f"Failed to fetch config from backend: {e}")
        logger.info("Falling back to local config")
        return _load_config_from_local()


def categorize_risk_level(risk_score: float) -> str:
    """Categorize risk score into risk level."""
    if risk_score < 0.25:
        return "Very Low"
    elif risk_score < 0.45:
        return "Low"
    elif risk_score < 0.65:
        return "Medium"
    elif risk_score < 0.85:
        return "High"
    else:
        return "Very High"


# ==================== Endpoints ====================


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Risk Score & Premium Planning",
        "version": "1.0.0",
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Predict risk score and generate insurance plans.

    Args:
        request: Prediction request with pincode, claim_history, and avg_income

    Returns:
        PredictionResponse with risk_score and available plans
    """
    request_id = str(uuid.uuid4())[:8]
    request_started_at = time.perf_counter()

    logger.info(
        "Predict request received | request_id=%s | pincode=%s | claim_history=%s | avg_income=%.2f",
        request_id,
        request.pincode,
        request.claim_history,
        request.avg_income,
    )

    try:
        # Step 1: Load model and config
        model = load_model()
        pricing_config = load_pricing_config()
        logger.info(
            "Step 1 complete | request_id=%s | model_features=%s | config_source=%s | plans_available=%s",
            request_id,
            getattr(model, "n_features_in_", "unknown"),
            settings.CONFIG_SOURCE,
            len(pricing_config.get("plans", {})),
        )

        # Step 2: Enrich data - get location info
        location_info = get_location_info(request.pincode)
        if not location_info:
            raise ValueError(f"Cannot find location for pincode {request.pincode}")
        logger.info(
            "Step 2 complete | request_id=%s | location_info=%s",
            request_id,
            json.dumps(location_info),
        )

        # Step 3: Get weather features
        weather_features = get_weather_features(
            location_info["lat"], location_info["lon"]
        )
        weather_source = weather_features.get("weather_source", "unknown")
        logger.info(
            "Step 3 complete | request_id=%s | weather_source=%s | weather_features=%s",
            request_id,
            weather_source,
            json.dumps(weather_features),
        )

        # Step 4: Create feature vector
        features_dict = create_features(
            location_info=location_info,
            weather_features=weather_features,
            claim_history=request.claim_history,
            avg_income=request.avg_income,
        )
        logger.info(
            "Step 4 complete | request_id=%s | engineered_features=%s",
            request_id,
            json.dumps(features_dict),
        )

        # Step 5: Predict risk score
        # Model expects features in this order from train.py
        feature_vector = [
            features_dict["risk_zone"],
            features_dict["rainy_hours_next_48h"],
            features_dict["avg_rainfall_next_48h"],
            features_dict["rainy_hours_last_24h"],
            features_dict["claim_history"],
            features_dict["avg_income"],
            features_dict["disruption_score"],
        ]

        logger.info(
            "Step 5 input | request_id=%s | feature_vector=%s",
            request_id,
            json.dumps(feature_vector),
        )

        raw_risk_score = float(model.predict([feature_vector])[0])
        risk_score = max(0, min(1, raw_risk_score))  # Clamp to [0, 1]
        logger.info(
            "Step 5 output | request_id=%s | raw_risk_score=%.6f | clamped_risk_score=%.6f",
            request_id,
            raw_risk_score,
            risk_score,
        )

        # Step 6: Generate plans
        plans_list = generate_plans(risk_score, pricing_config)
        logger.info(
            "Step 6 complete | request_id=%s | generated_plans=%s",
            request_id,
            json.dumps(plans_list),
        )

        # Convert to response format
        plans = [Plan(**plan) for plan in plans_list]

        # Create reasoning dictionary
        reasoning = {
            "risk_factors": {
                "location_risk": features_dict["risk_zone"],
                "rainy_hours_next_48h": features_dict["rainy_hours_next_48h"],
                "avg_rainfall_next_48h": features_dict["avg_rainfall_next_48h"],
                "rainy_hours_last_24h": features_dict["rainy_hours_last_24h"],
                "disruption_score": features_dict["disruption_score"],
                "claim_history": features_dict["claim_history"],
                "income_level": request.avg_income,
            }
        }

        response_payload = {
            "risk_score": risk_score,
            "risk_level": categorize_risk_level(risk_score),
            "plans_count": len(plans),
            "location": {
                "city": location_info.get("city"),
                "state": location_info.get("state"),
                "risk_zone": location_info.get("risk_zone"),
            },
            "reasoning": reasoning,
        }

        elapsed_ms = (time.perf_counter() - request_started_at) * 1000
        logger.info(
            "Predict request completed | request_id=%s | duration_ms=%.2f | response_summary=%s",
            request_id,
            elapsed_ms,
            json.dumps(response_payload),
        )

        return PredictionResponse(
            risk_score=risk_score,
            risk_level=categorize_risk_level(risk_score),
            plans=plans,
            location={
                "city": location_info.get("city"),
                "state": location_info.get("state"),
                "risk_zone": location_info.get("risk_zone"),
            },
            reasoning=reasoning,
        )

    except ValueError as e:
        logger.error(
            "Validation error | request_id=%s | pincode=%s | error=%s",
            request_id,
            request.pincode,
            e,
        )
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError as e:
        logger.error("Resource not found | request_id=%s | error=%s", request_id, e)
        raise HTTPException(status_code=500, detail="Model or config not found")

    except Exception as e:
        logger.error(
            "Prediction error | request_id=%s | pincode=%s | error=%s",
            request_id,
            request.pincode,
            e,
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/load-config")
async def reload_config():
    """Reload pricing configuration."""
    try:
        config = load_pricing_config()
        return {
            "status": "success",
            "message": "Configuration reloaded",
            "config_source": settings.CONFIG_SOURCE,
            "plans_count": len(config.get("plans", {})),
        }

    except Exception as e:
        logger.error(f"Error reloading config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config():
    """Get current pricing configuration."""
    try:
        config = load_pricing_config()
        return {"source": settings.CONFIG_SOURCE, "config": config}

    except Exception as e:
        logger.error(f"Error fetching config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Startup/Shutdown ====================


@app.on_event("startup")
async def startup_event():
    """Startup event - validate configuration."""
    try:
        logger.info("Starting ML service...")
        settings.validate()

        # Try to load model and config to fail fast
        load_model()
        load_pricing_config()

        logger.info("ML service started successfully!")

    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise


if __name__ == "__main__":
    # Run with: uvicorn main:app --reload --port 8001
    uvicorn.run(app, host=settings.ML_SERVICE_HOST, port=settings.ML_SERVICE_PORT)
