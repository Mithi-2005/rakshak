import unittest
from datetime import date, datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from accounts.db.base import Base
from accounts.models import User, UserProfile, UserRole
from claims.services.claim_service import (
    calculate_claim_amount,
    create_claims_for_unprocessed_triggers,
)
from policies.models import Policy, PolicyStatus
from policies.services.policy_service import sync_policy_status
from triggers.models import TriggerEvent, TriggerType


class Phase2ServiceTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        self.SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def test_sync_policy_status_marks_expired_policy(self):
        now = datetime.now(timezone.utc)
        policy = Policy(
            user_id=1,
            pincode="500001",
            plan_id="basic",
            coverage_amount=100,
            premium_amount=29,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 2),
            status=PolicyStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

        updated = sync_policy_status(policy)
        self.assertEqual(updated.status, PolicyStatus.EXPIRED)

    def test_claim_amount_respects_trigger_caps(self):
        amount = calculate_claim_amount(
            trigger_type=TriggerType.RAIN,
            severity=0.9,
            avg_daily_income=1200,
            coverage_amount=50000,
        )
        self.assertLessEqual(amount, 500.0)
        self.assertGreater(amount, 0)

    def test_nightly_claim_generation_creates_single_claim(self):
        session = self.SessionLocal()
        now = datetime.now(timezone.utc)

        user = User(
            name="Test User",
            email="worker@example.com",
            password_hash="hash",
            role=UserRole.USER,
            is_profile_completed=True,
            is_active=True,
            created_at=now,
        )
        session.add(user)
        session.flush()

        session.add(
            UserProfile(
                user_id=user.id,
                phone="9999999999",
                platform="Swiggy",
                city="Hyderabad",
                pincode="500001",
                vehicle_type="Bike",
                avg_daily_income=900,
                created_at=now,
                updated_at=now,
            )
        )

        policy = Policy(
            user_id=user.id,
            pincode="500001",
            plan_id="standard",
            coverage_amount=100000,
            premium_amount=49,
            start_date=now.date(),
            end_date=now.date(),
            status=PolicyStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        session.add(policy)
        session.flush()

        trigger = TriggerEvent(
            pincode="500001",
            trigger_type=TriggerType.RAIN,
            severity=0.8,
            threshold_value=12,
            observed_value=18,
            source_payload={"source": "test"},
            start_time=now,
            end_time=now,
            created_at=now,
            is_processed=False,
        )
        session.add(trigger)
        session.commit()

        created = create_claims_for_unprocessed_triggers(session, run_date=now.date())
        session.commit()

        self.assertEqual(created, 1)
        self.assertEqual(trigger.is_processed, True)


if __name__ == "__main__":
    unittest.main()
