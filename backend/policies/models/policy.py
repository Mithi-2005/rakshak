"""SQLAlchemy models for insurance policies."""

from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SAEnum, Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accounts.db.base import Base


class PolicyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class Policy(Base):
    __tablename__ = "policies"
    __table_args__ = (
        Index("ix_policies_user_status", "user_id", "status"),
        Index("ix_policies_pincode_status", "pincode", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    pincode: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    plan_id: Mapped[str] = mapped_column(String(30), nullable=False)
    coverage_amount: Mapped[float] = mapped_column(Float, nullable=False)
    premium_amount: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PolicyStatus] = mapped_column(
        SAEnum(PolicyStatus, name="policy_status"),
        nullable=False,
        default=PolicyStatus.ACTIVE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user = relationship("User", backref="policies")
    claims = relationship("Claim", back_populates="policy")

