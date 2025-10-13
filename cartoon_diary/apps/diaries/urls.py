"""Diary web routes."""

from django.urls import path

from .views import CalendarView


app_name = "diaries-web"

urlpatterns = [
    path("calendar/", CalendarView.as_view(), name="calendar"),
]
