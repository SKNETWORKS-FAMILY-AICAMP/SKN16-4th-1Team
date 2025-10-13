"""Simple retry helper."""

from __future__ import annotations

import time
from typing import Callable, TypeVar


F = TypeVar("F", bound=Callable[..., object])


def retry(*, attempts: int = 3, delay: float = 0.5) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(*args, **kwargs):  # type: ignore[misc]
            last_exc = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # pragma: no cover - fallback path
                    last_exc = exc
                    time.sleep(delay)
            if last_exc:
                raise last_exc

        return wrapper  # type: ignore[return-value]

    return decorator
