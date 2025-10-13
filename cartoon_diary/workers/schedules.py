"""Celery beat schedule definitions."""

from datetime import timedelta

from .queues import DEFAULT_QUEUE


BEAT_SCHEDULE = {
    "send-daily-reminders": {
        "task": "apps.diaries.tasks.send_diary_reminder_email",
        "schedule": timedelta(hours=24),
        "options": {"queue": DEFAULT_QUEUE},
    }
}
