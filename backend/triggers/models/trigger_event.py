"""SQLAlchemy models for trigger events."""

from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Boolean, DateTime, Enum as SAEnum, Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accounts.db.base import Base


class TriggerType(str, Enum):
    RAIN = "RAIN"
    AQI = "AQI"
    NEWS = "NEWS"


class TriggerEvent(Base):
    __tablename__ = "trigger_events"
    __table_args__ = (
        Index("ix_trigger_events_pincode_type", "pincode", "trigger_type"),
        Index("ix_trigger_events_processed", "is_processed"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pincode: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    trigger_type: Mapped[TriggerType] = mapped_column(
        SAEnum(TriggerType, name="trigger_type"), nullable=False
    )
    severity: Mapped[float] = mapped_column(Float, nullable=False)
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False)
    observed_value: Mapped[float] = mapped_column(Float, nullable=False)
    source_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    claims = relationship("Claim", back_populates="trigger_event")

