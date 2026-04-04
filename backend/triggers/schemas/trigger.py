"""Schemas for trigger APIs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TriggerEventOut(BaseModel):
    id: int
    pincode: str
    trigger_type: str
    severity: float
    threshold_value: float
    observed_value: float
    source_payload: dict
    start_time: datetime
    end_time: datetime | None
    created_at: datetime
    is_processed: bool

    model_config = ConfigDict(from_attributes=True)

