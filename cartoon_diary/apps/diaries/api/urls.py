"""API routing for diary endpoints."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DiaryEntryViewSet, DiaryEntryWriteViewSet


router = DefaultRouter()
router.register("", DiaryEntryViewSet, basename="diary")
router.register("write", DiaryEntryWriteViewSet, basename="diary-write")


app_name = "diaries-api"

urlpatterns = [
    path("", include(router.urls)),
]
