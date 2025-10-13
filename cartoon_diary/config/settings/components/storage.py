"""Storage defaults and overrides."""

import os


DEFAULT_FILE_STORAGE = os.getenv(
    "DJANGO_DEFAULT_FILE_STORAGE",
    "django.core.files.storage.FileSystemStorage",
)

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE,
        "OPTIONS": {
            "location": os.getenv("DJANGO_MEDIA_ROOT"),
        },
    }
}
