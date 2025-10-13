"""Diary models."""

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class DiaryEntry(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )
    date = models.DateField()
    title = models.CharField(max_length=120, blank=True)
    content = models.TextField()
    mood = models.CharField(max_length=32, blank=True)
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ("-date", "-created_at")

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"{self.user.email} @ {self.date}"
