"""Celery queue names."""

GENERATION_QUEUE = "generation"
DEFAULT_QUEUE = "default"

ROUTES = {
    "apps.generation.tasks.run_generation_pipeline": {"queue": GENERATION_QUEUE},
}
