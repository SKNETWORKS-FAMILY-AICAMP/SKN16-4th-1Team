"""Generation API routes."""

from django.urls import path

from .views import CartoonGenerateView, CartoonStatusView


app_name = "generation"

urlpatterns = [
    path("<int:diary_entry_id>/generate/", CartoonGenerateView.as_view(), name="generate"),
    path("<int:diary_entry_id>/", CartoonStatusView.as_view(), name="status"),
]
