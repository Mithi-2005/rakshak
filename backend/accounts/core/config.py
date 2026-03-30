"""Configuration helpers for auth module."""

from dataclasses import dataclass
import os
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int


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
)
