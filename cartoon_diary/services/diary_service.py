"""High-level diary orchestration services."""

from __future__ import annotations

from datetime import date

from django.db import transaction

from apps.diaries.services import save_diary_entry
from apps.generation.pipelines import trigger_cartoon_generation


@transaction.atomic
def save_entry_and_trigger_generation(
    *,
    user,
    entry_date: date,
    content: str,
    title: str | None = None,
    mood: str | None = None,
    tags: list[str] | None = None,
) -> None:
    entry = save_diary_entry(
        user=user,
        entry_date=entry_date,
        content=content,
        title=title,
        mood=mood,
        tags=tags,
    )
    trigger_cartoon_generation(diary_entry_id=entry.id)
