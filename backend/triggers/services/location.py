"""Deterministic pincode-to-location helpers for polling real APIs."""

from __future__ import annotations

from typing import Any


PINCODE_PREFIXES: dict[str, dict[str, Any]] = {
    "110": {"city": "New Delhi Region", "lat": 28.61, "lon": 77.21},
    "400": {"city": "Mumbai Region", "lat": 19.07, "lon": 72.88},
    "500": {"city": "Hyderabad Region", "lat": 17.38, "lon": 78.48},
    "560": {"city": "Bengaluru Region", "lat": 12.97, "lon": 77.59},
    "600": {"city": "Chennai Region", "lat": 13.08, "lon": 80.27},
    "682": {"city": "Kochi Region", "lat": 9.95, "lon": 76.28},
}


def get_location_for_pincode(pincode: str) -> dict[str, Any]:
    prefix = str(pincode).strip()[:3]
    suffix = int(str(pincode).strip()[3:])
    base = PINCODE_PREFIXES.get(
        prefix, {"city": "India Region", "lat": 22.97, "lon": 78.65}
    )
    lat_offset = ((suffix % 21) - 10) * 0.01
    lon_offset = (((suffix // 7) % 21) - 10) * 0.01
    return {
        "city": base["city"],
        "lat": round(base["lat"] + lat_offset, 4),
        "lon": round(base["lon"] + lon_offset, 4),
    }

