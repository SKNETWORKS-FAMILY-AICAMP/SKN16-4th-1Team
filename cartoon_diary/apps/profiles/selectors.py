"""Read helpers for profiles."""

from __future__ import annotations

from .models import Profile


def get_profile_for_user(*, user) -> Profile:
    profile, _created = Profile.objects.select_related("user").get_or_create(user=user)
    return profile
