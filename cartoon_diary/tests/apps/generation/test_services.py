"""Tests for generation services."""

from datetime import date

import pytest

from apps.diaries.services import save_diary_entry
from apps.generation.services import enqueue_generation


@pytest.mark.django_db
def test_enqueue_generation_creates_cartoon(user):
    entry = save_diary_entry(user=user, entry_date=date.today(), content="Hello")
    cartoon = enqueue_generation(diary_entry=entry)
    assert cartoon.status == cartoon.Status.QUEUED
