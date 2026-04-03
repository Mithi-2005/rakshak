"""
Plan generator module.
Generates dynamic pricing plans based on risk score and configuration.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def generate_plans(risk_score: float, config: Dict) -> List[Dict]:
    """
    Generate pricing plans based on risk score and pricing configuration.

    Args:
        risk_score: Risk score between 0 and 1
        config: Pricing configuration dict with base_price, multipliers, and plans

    Returns:
        List of plan dicts with plan_id, coverage, and premium
    """
    try:
        # Validate risk score
        risk_score = max(0, min(1, risk_score))

        # Extract configuration
        base_price = config.get("base_price", 40)
        risk_multiplier = config.get("risk_multiplier", 40)

        plans_config = config.get("plans", {})

        # Generate plans
        plans = []

        for plan_id, plan_config in plans_config.items():
            if not plan_config.get("is_active", True):
                continue  # Skip inactive plans

            plan = _calculate_plan(
                plan_id=plan_id,
                risk_score=risk_score,
                base_price=base_price,
                risk_multiplier=risk_multiplier,
                plan_config=plan_config,
            )

            if plan:
                plans.append(plan)

        # Sort by price (ascending)
        plans.sort(key=lambda x: x["premium"])

        return plans

    except Exception as e:
        logger.error(f"Error generating plans: {e}")
        raise


def _calculate_plan(
    plan_id: str,
    risk_score: float,
    base_price: float,
    risk_multiplier: float,
    plan_config: Dict,
) -> Dict:
    """
    Calculate a single plan's coverage and premium.

    Args:
        plan_id: Plan identifier (basic, standard, premium)
        risk_score: Risk score between 0 and 1
        base_price: Base price from config
        risk_multiplier: Risk multiplier from config
        plan_config: Plan-specific config

    Returns:
        Dict with plan details
    """
    try:
        coverage_multiplier = plan_config.get("coverage_multiplier", 1.0)
        price_multiplier = plan_config.get("price_multiplier", 1.0)

        # Calculate base coverage (in thousands)
        base_coverage = 100  # 100k base
        coverage = base_coverage * coverage_multiplier

        # Calculate premium
        # Premium = base_price + (risk_score * risk_multiplier) * price_multiplier
        risk_component = risk_score * risk_multiplier
        premium = (base_price + risk_component) * price_multiplier

        return {
            "plan_id": plan_id,
            "coverage": float(coverage),
            "premium": float(round(premium, 2)),
            "coverage_multiplier": coverage_multiplier,
            "price_multiplier": price_multiplier,
        }

    except Exception as e:
        logger.error(f"Error calculating plan {plan_id}: {e}")
        return None


def validate_plans(plans: List[Dict]) -> bool:
    """
    Validate generated plans.

    Args:
        plans: List of plan dicts

    Returns:
        True if valid, False otherwise
    """
    if not plans:
        logger.warning("No plans generated")
        return False

    for plan in plans:
        if "plan_id" not in plan or "coverage" not in plan or "premium" not in plan:
            logger.error(f"Invalid plan structure: {plan}")
            return False

        if plan["premium"] < 0:
            logger.error(f"Negative premium in plan {plan['plan_id']}")
            return False

        if plan["coverage"] < 0:
            logger.error(f"Negative coverage in plan {plan['plan_id']}")
            return False

    return True
