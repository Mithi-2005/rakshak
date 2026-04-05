"""SQLAlchemy models for claims."""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accounts.db.base import Base


class ClaimStatus(str, Enum):
    CREATED = "CREATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Claim(Base):
    __tablename__ = "claims"
    __table_args__ = (
        Index("ix_claims_user_status", "user_id", "status"),
        Index("ix_claims_policy_trigger", "policy_id", "trigger_event_id", unique=True),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    policy_id: Mapped[int] = mapped_column(
        ForeignKey("policies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    trigger_event_id: Mapped[int] = mapped_column(
        ForeignKey("trigger_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    claim_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[ClaimStatus] = mapped_column(
        SAEnum(ClaimStatus, name="claim_status"),
        nullable=False,
        default=ClaimStatus.CREATED,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    policy = relationship("Policy", back_populates="claims")
    trigger_event = relationship("TriggerEvent", back_populates="claims")

