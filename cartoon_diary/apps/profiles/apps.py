"""Profiles app config."""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.profiles"

    def ready(self) -> None:
        from . import signals  # noqa: F401
