"""Diary-related Celery tasks."""

from __future__ import annotations

from celery import shared_task


@shared_task
def send_diary_reminder_email(user_id: int) -> None:
    """Placeholder for diary reminder email task."""

    # TODO: implement reminder email logic
    return None
