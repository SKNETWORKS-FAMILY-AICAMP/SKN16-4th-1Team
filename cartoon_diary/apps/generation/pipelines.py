"""Higher-level orchestration utilities."""

from __future__ import annotations

from .tasks import run_generation_pipeline


def trigger_cartoon_generation(*, diary_entry_id: int) -> None:
    """Entry point used by views/services to enqueue generation."""

    run_generation_pipeline.delay(diary_entry_id)
