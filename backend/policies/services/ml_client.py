"""Client helpers for the FastAPI ML service."""

from __future__ import annotations

from typing import Any

import requests

from accounts.core.config import settings
from accounts.core.exceptions import APIError


def fetch_pricing_prediction(
    *, pincode: str, claim_history: int, avg_income: float
) -> dict[str, Any]:
    try:
        response = requests.post(
            f"{settings.ml_service_url.rstrip('/')}/predict",
            json={
                "pincode": pincode,
                "claim_history": claim_history,
                "avg_income": avg_income,
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else "ML service error"
        raise APIError(502, f"ML service request failed: {detail}") from exc
    except requests.RequestException as exc:
        raise APIError(503, "ML service is unavailable") from exc

