"""Celery tasks orchestrating the prompt/image pipeline."""

from __future__ import annotations

from django.utils import timezone
from celery import chain, shared_task

from apps.core.exceptions import IntegrationError
from apps.diaries.models import DiaryEntry

from .models import Cartoon, CartoonPanel, Prompt
from .services import mark_cartoon_failed


@shared_task
def generate_prompt_task(diary_entry_id: int) -> int:
    diary_entry = DiaryEntry.objects.get(pk=diary_entry_id)
    prompt = Prompt.objects.create(
        diary_entry=diary_entry,
        body={"story": diary_entry.content},
        model="gpt-4o-mini",
    )
    return prompt.pk


@shared_task
def generate_panels_task(prompt_id: int) -> int:
    prompt = Prompt.objects.get(pk=prompt_id)
    cartoon = Cartoon.objects.filter(diary_entry=prompt.diary_entry).order_by("-created_at").first()
    if not cartoon:
        raise IntegrationError("Cartoon record missing for prompt")
    cartoon.status = Cartoon.Status.RUNNING
    cartoon.save(update_fields=["status", "updated_at"])
    for index in range(1, 5):
        CartoonPanel.objects.create(cartoon=cartoon, index=index, image="", caption="")
    return cartoon.pk


@shared_task
def compose_grid_task(cartoon_id: int) -> int:
    cartoon = Cartoon.objects.get(pk=cartoon_id)
    cartoon.status = Cartoon.Status.SUCCEEDED
    cartoon.completed_at = timezone.now()
    cartoon.save(update_fields=["status", "completed_at", "updated_at"])
    return cartoon.pk


@shared_task
def run_generation_pipeline(diary_entry_id: int) -> None:
    cartoon = Cartoon.objects.create(diary_entry_id=diary_entry_id, status=Cartoon.Status.QUEUED)
    workflow = chain(
        generate_prompt_task.s(diary_entry_id),
        generate_panels_task.s(),
        compose_grid_task.s(),
    )
    try:
        workflow()  # kick off synchronous chain; Celery will async when broker configured
    except Exception as exc:  # pragma: no cover - pipeline failure path
        mark_cartoon_failed(cartoon=cartoon, reason=str(exc))
