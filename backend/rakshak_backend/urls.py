"""rakshak_backend URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.routes.auth")),
    path("user/", include("accounts.routes.user")),
    path("admin/", include("pricing_admin.urls")),  # Pricing Admin API
    path("policies/", include("policies.routes.policy")),
    path("claims/", include("claims.routes.claim")),
    path("triggers/", include("triggers.routes.trigger")),
]
