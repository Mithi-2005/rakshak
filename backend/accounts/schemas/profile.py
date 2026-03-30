"""Pydantic schemas for user profile endpoints."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileUpsertRequest(BaseModel):
    phone: Optional[str] = None
    platform: Optional[str] = None
    city: Optional[str] = None
    vehicle_type: Optional[str] = None
    avg_daily_income: Optional[float] = None


class UserProfileOut(BaseModel):
    user_id: int
    phone: Optional[str] = None
    platform: Optional[str] = None
    city: Optional[str] = None
    vehicle_type: Optional[str] = None
    avg_daily_income: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfileResponse(BaseModel):
    profile_completed: bool
    profile: Optional[UserProfileOut] = None
