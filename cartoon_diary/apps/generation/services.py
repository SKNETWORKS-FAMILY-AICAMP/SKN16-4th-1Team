"""Command helpers for generation pipeline."""

from __future__ import annotations

from django.utils import timezone

from apps.core.exceptions import GenerationError

from .models import Cartoon, Prompt


def enqueue_generation(*, diary_entry, prompt_payload: dict | None = None) -> Cartoon:
    """Create a queued cartoon record for asynchronous processing."""

    cartoon = Cartoon.objects.create(diary_entry=diary_entry, status=Cartoon.Status.QUEUED)
    if prompt_payload:
        Prompt.objects.create(
            diary_entry=diary_entry,
            body=prompt_payload,
            model=prompt_payload.get("model", "gpt-4o-mini"),
        )
    return cartoon


def mark_cartoon_failed(*, cartoon: Cartoon, reason: str) -> None:
    cartoon.status = Cartoon.Status.FAILED
    cartoon.fail_reason = reason
    cartoon.completed_at = timezone.now()
    cartoon.save(update_fields=["status", "fail_reason", "completed_at", "updated_at"])
    raise GenerationError(reason)
