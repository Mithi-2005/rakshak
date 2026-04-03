"""
Django admin configuration for pricing models
"""

from django.contrib import admin
from .models import PricingConfig, PricingPlan, PricingAuditLog


@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    """Admin interface for PricingConfig."""

    list_display = [
        "id",
        "base_price",
        "risk_multiplier",
        "income_factor",
        "is_active",
        "updated_at",
    ]
    list_filter = ["is_active", "updated_at"]
    search_fields = ["base_price"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Configuration",
            {"fields": ("base_price", "risk_multiplier", "income_factor")},
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    """Admin interface for PricingPlan."""

    list_display = [
        "plan_id",
        "coverage_multiplier",
        "price_multiplier",
        "is_active",
        "updated_at",
    ]
    list_filter = ["is_active", "plan_id", "updated_at"]
    search_fields = ["plan_id", "description"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Plan Details", {"fields": ("plan_id", "description")}),
        ("Multipliers", {"fields": ("coverage_multiplier", "price_multiplier")}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(PricingAuditLog)
class PricingAuditLogAdmin(admin.ModelAdmin):
    """Admin interface for PricingAuditLog."""

    list_display = [
        "action",
        "model_name",
        "object_id",
        "created_at",
    ]
    list_filter = ["action", "model_name", "created_at"]
    search_fields = ["model_name", "object_id"]
    readonly_fields = [
        "action",
        "model_name",
        "object_id",
        "changes",
        "created_at",
    ]

    def has_add_permission(self, request):
        """Prevent manual creation of audit logs."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of audit logs."""
        return False
