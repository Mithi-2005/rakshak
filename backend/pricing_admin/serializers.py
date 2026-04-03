"""
Django REST Framework serializers for pricing configuration
"""

from rest_framework import serializers
from .models import PricingConfig, PricingPlan, PricingAuditLog


class PricingConfigSerializer(serializers.ModelSerializer):
    """Serializer for PricingConfig model."""

    class Meta:
        model = PricingConfig
        fields = [
            "id",
            "base_price",
            "risk_multiplier",
            "income_factor",
            "is_active",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class PricingPlanSerializer(serializers.ModelSerializer):
    """Serializer for PricingPlan model."""

    class Meta:
        model = PricingPlan
        fields = [
            "id",
            "plan_id",
            "coverage_multiplier",
            "price_multiplier",
            "description",
            "is_active",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class PricingAuditLogSerializer(serializers.ModelSerializer):
    """Serializer for PricingAuditLog model."""

    class Meta:
        model = PricingAuditLog
        fields = [
            "id",
            "action",
            "model_name",
            "object_id",
            "changes",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "action",
            "model_name",
            "object_id",
            "changes",
            "created_at",
        ]


class PricingConfigExportSerializer(serializers.Serializer):
    """Serializer for exporting full pricing config as JSON."""

    base_price = serializers.FloatField()
    risk_multiplier = serializers.FloatField()
    income_factor = serializers.FloatField()
    plans = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()
    version = serializers.IntegerField(default=1)

    def get_plans(self, obj):
        """Get all active plans."""
        plans = PricingPlan.objects.all()
        plans_dict = {}
        for plan in plans:
            plans_dict[plan.plan_id] = {
                "coverage_multiplier": plan.coverage_multiplier,
                "price_multiplier": plan.price_multiplier,
                "is_active": plan.is_active,
                "description": plan.description,
            }
        return plans_dict

    def get_last_updated(self, obj):
        """Get last updated timestamp."""
        config = PricingConfig.objects.order_by("-updated_at").first()
        if config:
            return config.updated_at.isoformat()
        return None
