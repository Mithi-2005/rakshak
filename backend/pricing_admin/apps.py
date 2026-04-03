"""
App configuration for pricing_admin
"""

from django.apps import AppConfig


class PricingAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pricing_admin"
    verbose_name = "Pricing Administration"

    def ready(self):
        """Initialize app - ensure default pricing config exists."""
        from .models import PricingConfig, PricingPlan

        # Create default pricing config if none exists
        if not PricingConfig.objects.exists():
            config = PricingConfig.objects.create(
                base_price=40,
                risk_multiplier=40,
                income_factor=5,
                is_active=True,
            )

        # Create default plans if none exist
        default_plans = [
            {
                "plan_id": "basic",
                "coverage_multiplier": 0.5,
                "price_multiplier": 0.8,
                "description": "Basic coverage with essential protection",
            },
            {
                "plan_id": "standard",
                "coverage_multiplier": 1.0,
                "price_multiplier": 1.0,
                "description": "Standard coverage with balanced protection and premium",
            },
            {
                "plan_id": "premium",
                "coverage_multiplier": 1.5,
                "price_multiplier": 1.4,
                "description": "Premium coverage with maximum protection",
            },
        ]

        for plan_data in default_plans:
            PricingPlan.objects.get_or_create(
                plan_id=plan_data["plan_id"],
                defaults={
                    "coverage_multiplier": plan_data["coverage_multiplier"],
                    "price_multiplier": plan_data["price_multiplier"],
                    "description": plan_data["description"],
                    "is_active": True,
                },
            )
