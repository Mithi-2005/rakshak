"""
Django REST Framework views for pricing administration
"""

import json
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PricingConfig, PricingPlan, PricingAuditLog
from .serializers import (
    PricingConfigSerializer,
    PricingPlanSerializer,
    PricingAuditLogSerializer,
    PricingConfigExportSerializer,
)

logger = logging.getLogger(__name__)


class PricingConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing pricing configuration.

    Endpoints:
    - GET /admin/pricing-config/ -> Get current config
    - POST /admin/pricing-config/ -> Create new config
    - PUT /admin/pricing-config/{id} -> Update config
    - DELETE /admin/pricing-config/{id} -> Delete config
    - GET /admin/pricing-config/export/ -> Export as JSON
    """

    queryset = PricingConfig.objects.all()
    serializer_class = PricingConfigSerializer

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Get current active pricing configuration."""
        config = PricingConfig.objects.filter(is_active=True).first()

        if not config:
            return Response(
                {"error": "No active pricing configuration found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(config)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def export(self, request):
        """
        Export full pricing configuration as JSON.
        Compatible with ML service config format.
        """
        config = PricingConfig.objects.filter(is_active=True).first()

        if not config:
            return Response(
                {"error": "No active pricing configuration found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PricingConfigExportSerializer(config)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Activate a specific pricing configuration."""
        config = self.get_object()

        # Deactivate all others
        PricingConfig.objects.exclude(pk=config.pk).update(is_active=False)

        # Activate this one
        config.is_active = True
        config.save()

        # Log the action
        PricingAuditLog.objects.create(
            action="enable",
            model_name="PricingConfig",
            object_id=config.id,
            changes={"activated_config_id": config.id},
        )

        serializer = self.get_serializer(config)
        return Response(serializer.data)


class PricingPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing insurance plans.

    Endpoints:
    - GET /admin/plans/ -> List all plans
    - POST /admin/plans/ -> Create plan
    - PUT /admin/plans/{id} -> Update plan
    - DELETE /admin/plans/{id} -> Delete plan
    - POST /admin/plans/{id}/activate -> Enable plan
    - POST /admin/plans/{id}/deactivate -> Disable plan
    """

    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Enable a plan."""
        plan = self.get_object()
        plan.is_active = True
        plan.save()

        PricingAuditLog.objects.create(
            action="enable",
            model_name="PricingPlan",
            object_id=plan.id,
            changes={"plan_id": plan.plan_id},
        )

        serializer = self.get_serializer(plan)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """Disable a plan."""
        plan = self.get_object()
        plan.is_active = False
        plan.save()

        PricingAuditLog.objects.create(
            action="disable",
            model_name="PricingPlan",
            object_id=plan.id,
            changes={"plan_id": plan.plan_id},
        )

        serializer = self.get_serializer(plan)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Get all active plans."""
        plans = PricingPlan.objects.filter(is_active=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)


class PricingAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing audit logs.

    Endpoints:
    - GET /admin/audit-logs/ -> List all audit logs
    - GET /admin/audit-logs/{id} -> Get specific audit log
    """

    queryset = PricingAuditLog.objects.all()
    serializer_class = PricingAuditLogSerializer
    ordering = ["-created_at"]
