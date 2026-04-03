"""
URLs for pricing admin endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PricingConfigViewSet,
    PricingPlanViewSet,
    PricingAuditLogViewSet,
)

router = DefaultRouter()
router.register(r"pricing-config", PricingConfigViewSet)
router.register(r"plans", PricingPlanViewSet)
router.register(r"audit-logs", PricingAuditLogViewSet)

app_name = "pricing_admin"

urlpatterns = [
    path("", include(router.urls)),
]
