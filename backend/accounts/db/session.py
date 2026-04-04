"""Database engine and session utilities."""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from accounts.core.config import settings
from accounts.db.base import Base

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


@contextmanager
def get_db_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    # Import models before metadata creation so SQLAlchemy sees all tables.
    from accounts.models import User, UserProfile  # noqa: F401
    from policies.models import Policy  # noqa: F401
    from claims.models import Claim  # noqa: F401
    from triggers.models import TriggerEvent  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_phase2_schema()


def _ensure_phase2_schema() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "user_profiles" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("user_profiles")}
    if "pincode" in columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE user_profiles ADD COLUMN pincode VARCHAR(6)"))
