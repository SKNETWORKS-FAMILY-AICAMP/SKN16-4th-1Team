"""Command helpers for diary workflows."""

from __future__ import annotations

from datetime import date

from django.db import transaction

from .models import DiaryEntry


@transaction.atomic
def save_diary_entry(
    *,
    user,
    entry_date: date,
    content: str,
    title: str | None = None,
    mood: str | None = None,
    tags: list[str] | None = None,
) -> DiaryEntry:
    entry, _created = DiaryEntry.objects.update_or_create(
        user=user,
        date=entry_date,
        defaults={
            "content": content,
            "title": title or "",
            "mood": mood or "",
            "tags": tags or [],
        },
    )
    return entry
