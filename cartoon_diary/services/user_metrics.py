"""Metrics aggregation services."""

from __future__ import annotations

from datetime import date

from apps.diaries.models import DiaryEntry


def count_entries_for_range(*, user, start: date, end: date) -> int:
    return DiaryEntry.objects.filter(user=user, date__range=(start, end)).count()
