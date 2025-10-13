"""Development settings."""

from .base import *  # noqa: F401, F403

DEBUG = True

INSTALLED_APPS += ["django_extensions"]  # type: ignore[name-defined]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
