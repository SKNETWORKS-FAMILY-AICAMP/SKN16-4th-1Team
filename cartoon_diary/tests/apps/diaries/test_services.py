"""Tests for diary services."""

from datetime import date

import pytest

from apps.diaries.services import save_diary_entry


@pytest.mark.django_db
def test_save_diary_entry_creates_record(user):
    entry = save_diary_entry(
        user=user,
        entry_date=date.today(),
        content="Today was great",
    )
    assert entry.content == "Today was great"
