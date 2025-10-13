"""Utility script to load seed data for development."""

from datetime import date

from django.contrib.auth import get_user_model

from apps.diaries.services import save_diary_entry


def run() -> None:
    User = get_user_model()
    user, _ = User.objects.get_or_create(email="demo@example.com", defaults={"username": "demo"})
    user.set_password("demo1234")
    user.save()
    save_diary_entry(user=user, entry_date=date.today(), content="Sample diary entry.")


if __name__ == "__main__":
    run()
