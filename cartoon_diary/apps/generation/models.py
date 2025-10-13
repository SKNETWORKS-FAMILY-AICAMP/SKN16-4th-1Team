"""Models for the cartoon generation pipeline."""

from django.db import models

from apps.core.models import TimeStampedModel
from apps.diaries.models import DiaryEntry


class Prompt(TimeStampedModel):
    diary_entry = models.ForeignKey(
        DiaryEntry,
        on_delete=models.CASCADE,
        related_name="prompts",
    )
    body = models.JSONField(default=dict)
    model = models.CharField(max_length=100)
    params = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"Prompt for diary {self.diary_entry_id}"


class Cartoon(TimeStampedModel):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    diary_entry = models.ForeignKey(
        DiaryEntry,
        on_delete=models.CASCADE,
        related_name="cartoons",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    seed = models.CharField(max_length=64, blank=True)
    guidance_scale = models.FloatField(null=True, blank=True)
    grid_image = models.ImageField(upload_to="cartoons/grids/", blank=True, null=True)
    fail_reason = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"Cartoon {self.pk} ({self.status})"


class CartoonPanel(TimeStampedModel):
    cartoon = models.ForeignKey(
        Cartoon,
        on_delete=models.CASCADE,
        related_name="panels",
    )
    index = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="cartoons/panels/", blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("cartoon", "index")
        ordering = ("index",)

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"Panel {self.index} of cartoon {self.cartoon_id}"
