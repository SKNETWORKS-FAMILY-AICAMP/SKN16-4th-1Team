"""Celery application instance."""

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("cartoon_diary")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):  # type: ignore[override]
    """Simple debug task to confirm Celery setup."""

    print(f"Request: {self.request!r}")
