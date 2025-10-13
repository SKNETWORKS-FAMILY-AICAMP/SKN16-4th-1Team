"""Read helpers for cartoon generation."""

from __future__ import annotations

from .models import Cartoon


def get_latest_cartoon_for_entry(*, diary_entry_id: int) -> Cartoon | None:
    return (
        Cartoon.objects.filter(diary_entry_id=diary_entry_id)
        .select_related("diary_entry")
        .order_by("-version")
        .first()
    )
