"""
Django models for pricing configuration
"""

from django.db import models
from django.utils import timezone


class PricingConfig(models.Model):
    """
    Main pricing configuration model.
    Stores base pricing parameters used across all plans.
    """

    base_price = models.FloatField(default=40, help_text="Base premium price in INR")
    risk_multiplier = models.FloatField(
        default=40, help_text="Multiplier for risk score component"
    )
    income_factor = models.FloatField(
        default=5, help_text="Factor for income-based adjustments"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this config is currently active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pricing Configuration"
        verbose_name_plural = "Pricing Configurations"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Config (Base: ₹{self.base_price}, Risk: {self.risk_multiplier})"

    def to_dict(self):
        """Convert to dictionary for API response."""
        return {
            "id": self.id,
            "base_price": self.base_price,
            "risk_multiplier": self.risk_multiplier,
            "income_factor": self.income_factor,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat(),
        }


class PricingPlan(models.Model):
    """
    Individual insurance plan configuration.
    Manages plan-specific multipliers for coverage and pricing.
    """

    PLAN_CHOICES = [
        ("basic", "Basic Plan"),
        ("standard", "Standard Plan"),
        ("premium", "Premium Plan"),
    ]

    plan_id = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        unique=True,
        help_text="Unique plan identifier",
    )
    coverage_multiplier = models.FloatField(
        default=1.0, help_text="Multiplier for base coverage amount"
    )
    price_multiplier = models.FloatField(
        default=1.0, help_text="Multiplier for calculated premium"
    )
    description = models.TextField(blank=True, help_text="Description of the plan")
    is_active = models.BooleanField(
        default=True, help_text="Whether this plan is currently available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pricing Plan"
        verbose_name_plural = "Pricing Plans"
        ordering = ["plan_id"]

    def __str__(self):
        return f"{self.get_plan_id_display()} (Coverage: {self.coverage_multiplier}x, Price: {self.price_multiplier}x)"

    def to_dict(self):
        """Convert to dictionary for API response."""
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "coverage_multiplier": self.coverage_multiplier,
            "price_multiplier": self.price_multiplier,
            "description": self.description,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat(),
        }


class PricingAuditLog(models.Model):
    """
    Audit log for tracking pricing configuration changes.
    """

    ACTION_CHOICES = [
        ("create", "Created"),
        ("update", "Updated"),
        ("delete", "Deleted"),
        ("enable", "Enabled"),
        ("disable", "Disabled"),
    ]

    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, help_text="Action performed"
    )
    model_name = models.CharField(
        max_length=50, help_text="Model affected (PricingConfig, PricingPlan)"
    )
    object_id = models.IntegerField(help_text="ID of affected object")
    changes = models.JSONField(default=dict, help_text="Details of changes made")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action.upper()} - {self.model_name} ({self.object_id})"
