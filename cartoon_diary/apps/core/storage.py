"""Storage helpers."""

from __future__ import annotations

from django.core.files.storage import get_storage_class


def get_media_storage():
    """Return the configured default file storage instance."""

    storage_cls = get_storage_class()
    return storage_cls()
