"""Schemas for claims APIs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClaimOut(BaseModel):
    id: int
    user_id: int
    policy_id: int
    trigger_event_id: int
    claim_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

