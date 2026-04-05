"""Pincode mapping for location enrichment and risk-zone estimation."""

from typing import Dict, Optional


PINCODE_DATABASE = {
    # Chennai
    "600001": {
        "city": "Chennai",
        "state": "Tamil Nadu",
        "lat": 13.0827,
        "lon": 80.2707,
        "risk_zone": 0.8,
        "zone_type": "coastal",
    },
    "600004": {
        "city": "Chennai",
        "state": "Tamil Nadu",
        "lat": 13.0476,
        "lon": 80.2754,
        "risk_zone": 0.75,
        "zone_type": "coastal",
    },
    # Mumbai
    "400001": {
        "city": "Mumbai",
        "state": "Maharashtra",
        "lat": 18.9667,
        "lon": 72.8333,
        "risk_zone": 0.9,
        "zone_type": "coastal",
    },
    "400004": {
        "city": "Mumbai",
        "state": "Maharashtra",
        "lat": 18.9650,
        "lon": 72.8395,
        "risk_zone": 0.85,
        "zone_type": "coastal",
    },
    # Delhi
    "110001": {
        "city": "New Delhi",
        "state": "Delhi",
        "lat": 28.6139,
        "lon": 77.2090,
        "risk_zone": 0.5,
        "zone_type": "urban",
    },
    "110002": {
        "city": "New Delhi",
        "state": "Delhi",
        "lat": 28.6308,
        "lon": 77.2197,
        "risk_zone": 0.45,
        "zone_type": "urban",
    },
    # Bangalore
    "560001": {
        "city": "Bangalore",
        "state": "Karnataka",
        "lat": 12.9716,
        "lon": 77.5946,
        "risk_zone": 0.6,
        "zone_type": "urban",
    },
    "560002": {
        "city": "Bangalore",
        "state": "Karnataka",
        "lat": 12.9679,
        "lon": 77.5899,
        "risk_zone": 0.55,
        "zone_type": "urban",
    },
    # Hyderabad
    "500001": {
        "city": "Hyderabad",
        "state": "Telangana",
        "lat": 17.3850,
        "lon": 78.4867,
        "risk_zone": 0.7,
        "zone_type": "urban",
    },
    "500002": {
        "city": "Hyderabad",
        "state": "Telangana",
        "lat": 17.3912,
        "lon": 78.4747,
        "risk_zone": 0.65,
        "zone_type": "urban",
    },
    # User-tested pincodes
    "682001": {
        "city": "Kochi",
        "state": "Kerala",
        "lat": 9.9312,
        "lon": 76.2673,
        "risk_zone": 0.86,
        "zone_type": "coastal",
    },
    "575006": {
        "city": "Mangaluru",
        "state": "Karnataka",
        "lat": 12.9141,
        "lon": 74.8560,
        "risk_zone": 0.82,
        "zone_type": "coastal",
    },
    "751001": {
        "city": "Bhubaneswar",
        "state": "Odisha",
        "lat": 20.2961,
        "lon": 85.8245,
        "risk_zone": 0.72,
        "zone_type": "urban",
    },
    "524315": {
        "city": "Nellore",
        "state": "Andhra Pradesh",
        "lat": 14.4426,
        "lon": 79.9865,
        "risk_zone": 0.68,
        "zone_type": "semi-urban",
    },
}


PINCODE_PREFIX_DATABASE = {
    # first-3-digit prefix -> representative centroid and baseline risk
    "682": {
        "city": "Kochi Region",
        "state": "Kerala",
        "lat": 9.95,
        "lon": 76.28,
        "risk_zone": 0.84,
        "zone_type": "coastal",
    },
    "575": {
        "city": "Mangaluru Region",
        "state": "Karnataka",
        "lat": 12.91,
        "lon": 74.85,
        "risk_zone": 0.80,
        "zone_type": "coastal",
    },
    "751": {
        "city": "Bhubaneswar Region",
        "state": "Odisha",
        "lat": 20.30,
        "lon": 85.82,
        "risk_zone": 0.71,
        "zone_type": "urban",
    },
    "524": {
        "city": "Nellore Region",
        "state": "Andhra Pradesh",
        "lat": 14.45,
        "lon": 79.99,
        "risk_zone": 0.66,
        "zone_type": "semi-urban",
    },
    "110": {
        "city": "New Delhi Region",
        "state": "Delhi",
        "lat": 28.61,
        "lon": 77.21,
        "risk_zone": 0.50,
        "zone_type": "urban",
    },
    "560": {
        "city": "Bengaluru Region",
        "state": "Karnataka",
        "lat": 12.97,
        "lon": 77.59,
        "risk_zone": 0.58,
        "zone_type": "urban",
    },
    "600": {
        "city": "Chennai Region",
        "state": "Tamil Nadu",
        "lat": 13.08,
        "lon": 80.27,
        "risk_zone": 0.79,
        "zone_type": "coastal",
    },
    "400": {
        "city": "Mumbai Region",
        "state": "Maharashtra",
        "lat": 19.07,
        "lon": 72.88,
        "risk_zone": 0.88,
        "zone_type": "coastal",
    },
    "500": {
        "city": "Hyderabad Region",
        "state": "Telangana",
        "lat": 17.38,
        "lon": 78.48,
        "risk_zone": 0.67,
        "zone_type": "urban",
    },
}


def get_location_info(pincode: str) -> Optional[Dict]:
    """
    Get location information for a given pincode.

    Args:
        pincode: 6-digit pincode string

    Returns:
        Dict with city, coordinates, and risk_zone, or None if not found
    """
    if not pincode:
        return None

    # Clean pincode
    clean_pincode = str(pincode).strip()

    if clean_pincode in PINCODE_DATABASE:
        return PINCODE_DATABASE[clean_pincode]

    # Derive a deterministic regional estimate for unknown pincodes.
    return _derive_location_from_prefix(clean_pincode)


def _derive_location_from_prefix(clean_pincode: str) -> Dict:
    """Create deterministic location estimate from pincode prefix and suffix."""
    prefix = clean_pincode[:3]
    suffix = int(clean_pincode[3:])

    base = PINCODE_PREFIX_DATABASE.get(
        prefix,
        {
            "city": "Unknown Region",
            "state": "Unknown",
            "lat": 22.9734,
            "lon": 78.6569,
            "risk_zone": 0.55,
            "zone_type": "unknown",
        },
    )

    # Add small deterministic offsets so different pincodes within a region differ.
    lat_offset = ((suffix % 41) - 20) * 0.01
    lon_offset = (((suffix // 3) % 41) - 20) * 0.01
    risk_offset = ((suffix % 17) - 8) * 0.005

    return {
        "city": base["city"],
        "state": base["state"],
        "lat": round(base["lat"] + lat_offset, 4),
        "lon": round(base["lon"] + lon_offset, 4),
        "risk_zone": round(min(0.98, max(0.2, base["risk_zone"] + risk_offset)), 3),
        "zone_type": base["zone_type"],
    }


def validate_pincode(pincode: str) -> bool:
    """
    Validate if pincode format is correct.

    Args:
        pincode: Pincode string to validate

    Returns:
        True if valid, False otherwise
    """
    if not pincode:
        return False

    clean_pincode = str(pincode).strip()

    # Check if exactly 6 digits
    if len(clean_pincode) != 6 or not clean_pincode.isdigit():
        return False

    return True
