"""Configuration helpers for backend services."""

from dataclasses import dataclass
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    redis_url: str
    ml_service_url: str
    weather_base_url: str
    waqi_base_url: str
    waqi_api_token: str
    aqi_fallback_source: str
    news_api_base_url: str
    news_api_key: str
    news_query: str
    rain_trigger_threshold: float
    aqi_trigger_threshold: int
    news_trigger_threshold: float
    claim_cap_rain: float
    claim_cap_aqi: float
    claim_cap_news: float
    celery_broker_url: str
    celery_result_backend: str
    external_requests_verify_ssl: bool


def _build_database_url() -> str:
    env_database_url = os.getenv("DATABASE_URL")
    if env_database_url:
        return env_database_url

    db_name = os.getenv("DB_NAME", "rakshak_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    encoded_user = quote_plus(db_user)
    encoded_password = quote_plus(db_password)
    return f"postgresql+psycopg://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"


settings = Settings(
    database_url=_build_database_url(),
    jwt_secret_key=os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me")),
    jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")),
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    ml_service_url=os.getenv("ML_SERVICE_URL", "http://localhost:8001"),
    weather_base_url=os.getenv(
        "WEATHER_BASE_URL", "https://api.open-meteo.com/v1/forecast"
    ),
    waqi_base_url=os.getenv("WAQI_BASE_URL", "https://api.waqi.info/feed/geo"),
    waqi_api_token=os.getenv("WAQI_API_TOKEN", ""),
    aqi_fallback_source=os.getenv("AQI_FALLBACK_SOURCE", "openmeteo"),
    news_api_base_url=os.getenv(
        "NEWS_API_BASE_URL", "https://newsapi.org/v2/everything"
    ),
    news_api_key=os.getenv("NEWS_API_KEY", ""),
    news_query=os.getenv("NEWS_QUERY", "bandh OR strike OR curfew"),
    rain_trigger_threshold=float(os.getenv("RAIN_TRIGGER_THRESHOLD", "12.0")),
    aqi_trigger_threshold=int(os.getenv("AQI_TRIGGER_THRESHOLD", "300")),
    news_trigger_threshold=float(os.getenv("NEWS_TRIGGER_THRESHOLD", "0.75")),
    claim_cap_rain=float(os.getenv("CLAIM_CAP_RAIN", "600")),
    claim_cap_aqi=float(os.getenv("CLAIM_CAP_AQI", "500")),
    claim_cap_news=float(os.getenv("CLAIM_CAP_NEWS", "750")),
    celery_broker_url=os.getenv(
        "CELERY_BROKER_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ),
    celery_result_backend=os.getenv(
        "CELERY_RESULT_BACKEND", os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ),
    external_requests_verify_ssl=os.getenv(
        "EXTERNAL_REQUESTS_VERIFY_SSL", "true"
    ).lower()
    not in {"0", "false", "no"},
)
