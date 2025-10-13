"""Command helpers for profile manipulation."""

from __future__ import annotations

from .models import Profile


def update_profile(*, profile: Profile, **attrs) -> Profile:
    if attrs:
        for field, value in attrs.items():
            setattr(profile, field, value)
        profile.save(update_fields=list(attrs.keys()))
    return profile
