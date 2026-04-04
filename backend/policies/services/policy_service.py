"""Policy domain services."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from accounts.core.exceptions import APIError
from accounts.models import User, UserProfile
from claims.models import Claim
from policies.models import Policy, PolicyStatus
from triggers.models import TriggerEvent

from .ml_client import fetch_pricing_prediction


def ensure_profile_ready(user: User, db: Session) -> UserProfile:
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if profile is None:
        raise APIError(400, "Complete your profile before buying a policy")
    if not profile.pincode:
        raise APIError(400, "Profile pincode is required")
    if not profile.avg_daily_income or profile.avg_daily_income <= 0:
        raise APIError(400, "Average daily income is required")
    return profile


def get_claim_history_count(user_id: int, db: Session) -> int:
    return int(
        db.scalar(select(func.count(Claim.id)).where(Claim.user_id == user_id)) or 0
    )


def get_prediction_for_user(user: User, db: Session) -> dict:
    profile = ensure_profile_ready(user, db)
    return fetch_pricing_prediction(
        pincode=profile.pincode,
        claim_history=get_claim_history_count(user.id, db),
        avg_income=float(profile.avg_daily_income),
    )


def get_active_policy(user_id: int, db: Session) -> Policy | None:
    today = date.today()
    return db.scalar(
        select(Policy)
        .where(Policy.user_id == user_id)
        .where(Policy.status == PolicyStatus.ACTIVE)
        .where(Policy.end_date >= today)
        .order_by(Policy.end_date.desc())
    )


def sync_policy_status(policy: Policy) -> Policy:
    if policy.status == PolicyStatus.ACTIVE and policy.end_date < date.today():
        policy.status = PolicyStatus.EXPIRED
        policy.updated_at = datetime.now(timezone.utc)
    return policy


def list_user_policies(user_id: int, db: Session) -> list[Policy]:
    policies = list(
        db.scalars(
            select(Policy)
            .where(Policy.user_id == user_id)
            .order_by(Policy.created_at.desc())
        )
    )
    for policy in policies:
        sync_policy_status(policy)
    return policies


def purchase_policy(
    *,
    user: User,
    plan_id: str,
    coverage_amount: float,
    premium_amount: float,
    duration_days: int,
    db: Session,
) -> Policy:
    prediction = get_prediction_for_user(user, db)
    plan = next(
        (item for item in prediction.get("plans", []) if item["plan_id"] == plan_id),
        None,
    )
    if plan is None:
        raise APIError(400, "Selected plan is unavailable")

    if abs(float(plan["coverage"]) - coverage_amount) > 0.01 or abs(
        float(plan["premium"]) - premium_amount
    ) > 0.01:
        raise APIError(400, "Selected plan values are stale. Refresh plans and try again.")

    profile = ensure_profile_ready(user, db)
    current = get_active_policy(user.id, db)
    if current is not None:
        raise APIError(409, "An active policy already exists for this user")

    now = datetime.now(timezone.utc)
    start_date = now.date()
    policy = Policy(
        user_id=user.id,
        pincode=profile.pincode,
        plan_id=plan_id,
        coverage_amount=coverage_amount,
        premium_amount=premium_amount,
        start_date=start_date,
        end_date=start_date + timedelta(days=duration_days),
        status=PolicyStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )
    db.add(policy)
    db.flush()
    return policy


def get_dashboard_payload(user: User, db: Session) -> dict:
    profile = ensure_profile_ready(user, db)
    prediction = get_prediction_for_user(user, db)
    active_policy = get_active_policy(user.id, db)
    if active_policy is not None:
        sync_policy_status(active_policy)

    recent_claims_count = int(
        db.scalar(select(func.count(Claim.id)).where(Claim.user_id == user.id)) or 0
    )
    open_triggers_count = int(
        db.scalar(
            select(func.count(TriggerEvent.id))
            .where(TriggerEvent.pincode == profile.pincode)
            .where(TriggerEvent.end_time.is_(None))
        )
        or 0
    )

    return {
        "risk_score": prediction.get("risk_score", 0.0),
        "risk_level": prediction.get("risk_level", "Unknown"),
        "active_policy": active_policy,
        "recent_claims_count": recent_claims_count,
        "open_triggers_count": open_triggers_count,
        "plans": prediction.get("plans", []),
    }

