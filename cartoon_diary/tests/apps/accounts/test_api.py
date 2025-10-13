"""Tests for account endpoints."""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_signup_creates_user():
    client = APIClient()
    response = client.post(
        reverse("accounts:signup"),
        {"email": "new@example.com", "password": "pass1234", "username": "new"},
        format="json",
    )
    assert response.status_code == 201
