"""Schemas for policy and pricing endpoints."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PolicyPurchaseRequest(BaseModel):
    plan_id: str = Field(min_length=1, max_length=30)
    coverage_amount: float = Field(gt=0)
    premium_amount: float = Field(gt=0)
    duration_days: int = Field(default=7, ge=1, le=31)


class PolicyOut(BaseModel):
    id: int
    user_id: int
    pincode: str
    plan_id: str
    coverage_amount: float
    premium_amount: float
    start_date: date
    end_date: date
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PricingPlanOut(BaseModel):
    plan_id: str
    coverage: float
    premium: float
    coverage_multiplier: float | None = None
    price_multiplier: float | None = None


class PolicyDashboardResponse(BaseModel):
    risk_score: float
    risk_level: str
    active_policy: PolicyOut | None
    recent_claims_count: int
    open_triggers_count: int
    plans: list[PricingPlanOut]

