"""Profile endpoints."""

from django.urls import path

from .views import MeProfileView


app_name = "profiles"

urlpatterns = [
    path("me/", MeProfileView.as_view(), name="me"),
]
