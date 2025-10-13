"""Production settings."""

from .base import *  # noqa: F401, F403


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGGING["loggers"]["django.request"]["level"] = "WARNING"  # type: ignore[name-defined]
