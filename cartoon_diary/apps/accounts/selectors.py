"""Read-model helpers for accounts."""

from __future__ import annotations

from django.contrib.auth import get_user_model


User = get_user_model()


def get_user_by_email(email: str):
    """Return the first user matching the supplied email."""

    return User.objects.filter(email=email).first()
