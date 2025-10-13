"""Query helpers for diaries."""

from __future__ import annotations

from datetime import date

from apps.core.utils import get_month_bounds

from .models import DiaryEntry


def list_entries_for_month(*, user, month: date):
    start, end = get_month_bounds(month)
    return (
        DiaryEntry.objects.filter(user=user, date__range=(start, end))
        .order_by("date")
        .select_related("user")
    )
