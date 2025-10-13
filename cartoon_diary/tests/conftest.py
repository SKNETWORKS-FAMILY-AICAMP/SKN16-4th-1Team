"""Pytest fixtures."""

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(email="user@example.com", username="user", password="password")
