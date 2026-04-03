"""
Environment configuration loader for ML service.
All external configurations are loaded from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Determine project root: config_loader.py is in ai_models/utils/
# So we go up 3 levels to get to the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
AI_MODELS_DIR = PROJECT_ROOT / "ai_models"

# Load environment variables from .env file in ai_models directory
ENV_FILE = AI_MODELS_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Fallback to default .env in current directory
    load_dotenv()


class Settings:
    """Configuration settings loaded from environment variables."""

    # Weather API Configuration (Open-Meteo, no API key required)
    WEATHER_BASE_URL = os.getenv(
        "WEATHER_BASE_URL", "https://api.open-meteo.com/v1/forecast"
    )

    # Backend Configuration
    BACKEND_CONFIG_URL = os.getenv(
        "BACKEND_CONFIG_URL", "http://localhost:8000/admin/pricing-config"
    )

    # Model Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "ai_models/model/risk_model.pkl")

    # Pricing Config Path
    PRICING_CONFIG_PATH = os.getenv(
        "PRICING_CONFIG_PATH", "ai_models/config/pricing_config.json"
    )

    # Config Source: 'local' (JSON file) or 'backend' (API)
    CONFIG_SOURCE = os.getenv("CONFIG_SOURCE", "local")

    # API Server Configuration
    ML_SERVICE_HOST = os.getenv("ML_SERVICE_HOST", "0.0.0.0")
    ML_SERVICE_PORT = int(os.getenv("ML_SERVICE_PORT", "8001"))

    @classmethod
    def _resolve_path(cls, path_str: str) -> Path:
        """Resolve a path relative to the project root if it's a relative path."""
        path = Path(path_str)
        # If path is relative, resolve it relative to project root
        if not path.is_absolute():
            resolved_path = PROJECT_ROOT / path_str
            return resolved_path
        return path

    @classmethod
    def validate(cls):
        """Validate critical configuration."""
        if cls.CONFIG_SOURCE == "backend" and not cls.BACKEND_CONFIG_URL:
            raise ValueError(
                "BACKEND_CONFIG_URL must be set when CONFIG_SOURCE=backend"
            )

        if cls.CONFIG_SOURCE == "local":
            config_path = cls._resolve_path(cls.PRICING_CONFIG_PATH)
            if not config_path.exists():
                raise FileNotFoundError(
                    f"Pricing config not found at {config_path} (resolved from {cls.PRICING_CONFIG_PATH})"
                )


settings = Settings()
