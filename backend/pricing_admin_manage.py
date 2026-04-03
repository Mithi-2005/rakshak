"""
Management utilities for the pricing admin system.
Helpful scripts for initialization, testing, and maintenance.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rakshak_backend.settings")
django.setup()

from pricing_admin.models import PricingConfig, PricingPlan, PricingAuditLog


def initialize_default_config():
    """Initialize default pricing configuration."""
    print("Initializing default pricing configuration...")

    # Create default config if none exists
    config, created = PricingConfig.objects.get_or_create(
        is_active=True,
        defaults={
            "base_price": 40,
            "risk_multiplier": 40,
            "income_factor": 5,
        },
    )

    if created:
        print(f"✓ Created default PricingConfig: {config}")
    else:
        print(f"✓ Default PricingConfig already exists: {config}")

    # Create default plans
    plans_data = [
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

    for plan_data in plans_data:
        plan, created = PricingPlan.objects.get_or_create(
            plan_id=plan_data["plan_id"], defaults=plan_data
        )
        status = "Created" if created else "Already exists"
        print(f"✓ {status}: {plan}")

    print("\n✓ Default configuration initialized successfully!")


def display_current_config():
    """Display current active configuration."""
    print("\n═══════════════════════════════════════")
    print("Current Active Pricing Configuration")
    print("═══════════════════════════════════════\n")

    config = PricingConfig.objects.filter(is_active=True).first()

    if not config:
        print("✗ No active configuration found")
        return

    print(f"Configuration ID: {config.id}")
    print(f"Base Price: ₹{config.base_price}")
    print(f"Risk Multiplier: {config.risk_multiplier}")
    print(f"Income Factor: {config.income_factor}")
    print(f"Status: {'Active' if config.is_active else 'Inactive'}")
    print(f"Updated: {config.updated_at}\n")

    print("─────────────────────────────────────")
    print("Insurance Plans")
    print("─────────────────────────────────────\n")

    plans = PricingPlan.objects.all().order_by("plan_id")

    for plan in plans:
        status = "✓ Active" if plan.is_active else "✗ Inactive"
        print(f"{plan.plan_id.upper()}")
        print(f"  {status}")
        print(f"  Coverage Multiplier: {plan.coverage_multiplier}x")
        print(f"  Price Multiplier: {plan.price_multiplier}x")
        print(f"  {plan.description}\n")


def display_audit_logs(limit: int = 10):
    """Display recent audit logs."""
    print(f"\n═══════════════════════════════════════")
    print(f"Recent Audit Logs (Last {limit})")
    print("═══════════════════════════════════════\n")

    logs = PricingAuditLog.objects.all().order_by("-created_at")[:limit]

    if not logs:
        print("No audit logs found")
        return

    for log in logs:
        print(f"ID: {log.id}")
        print(f"Action: {log.action.upper()}")
        print(f"Model: {log.model_name}")
        print(f"Object ID: {log.object_id}")
        print(f"Timestamp: {log.created_at}")
        print(f"Changes: {log.changes}\n")


def clear_all_data():
    """⚠️  DANGEROUS: Clear all pricing configurations."""
    response = input(
        "⚠️  WARNING: This will delete all pricing configs and plans!\n"
        "Type 'YES' to confirm: "
    )

    if response.upper() != "YES":
        print("✗ Cancelled")
        return

    count_config = PricingConfig.objects.all().delete()[0]
    count_plans = PricingPlan.objects.all().delete()[0]
    count_logs = PricingAuditLog.objects.all().delete()[0]

    print(f"\n✓ Deleted:")
    print(f"  {count_config} PricingConfig records")
    print(f"  {count_plans} PricingPlan records")
    print(f"  {count_logs} Audit logs")


def export_config_to_json():
    """Export current config to JSON file."""
    import json
    from datetime import datetime

    config = PricingConfig.objects.filter(is_active=True).first()

    if not config:
        print("✗ No active configuration found")
        return

    plans = PricingPlan.objects.all()

    data = {
        "base_price": config.base_price,
        "risk_multiplier": config.risk_multiplier,
        "income_factor": config.income_factor,
        "plans": {
            plan.plan_id: {
                "coverage_multiplier": plan.coverage_multiplier,
                "price_multiplier": plan.price_multiplier,
                "is_active": plan.is_active,
                "description": plan.description,
            }
            for plan in plans
        },
        "last_updated": datetime.now().isoformat(),
        "version": 1,
    }

    filename = "pricing_config_export.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ Configuration exported to {filename}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pricing Admin Management Utilities")
    parser.add_argument(
        "command",
        choices=[
            "init",
            "display",
            "logs",
            "export",
            "clear",
        ],
        help="Command to execute",
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="Limit for audit logs (default: 10)"
    )

    args = parser.parse_args()

    if args.command == "init":
        initialize_default_config()
    elif args.command == "display":
        display_current_config()
    elif args.command == "logs":
        display_audit_logs(args.limit)
    elif args.command == "export":
        export_config_to_json()
    elif args.command == "clear":
        clear_all_data()
