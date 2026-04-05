"""Compatibility URL include for accounts package."""

from django.urls import include, path

urlpatterns = [
    path("auth/", include("accounts.routes.auth")),
    path("user/", include("accounts.routes.user")),
]
