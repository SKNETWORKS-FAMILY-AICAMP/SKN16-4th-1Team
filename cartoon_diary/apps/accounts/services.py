"""Command-layer helpers for accounts."""

from __future__ import annotations

from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(*, email: str, password: str, username: str | None = None) -> User:
    """Create a user using Django's password hashing."""

    return User.objects.create_user(email=email, password=password, username=username or email)
