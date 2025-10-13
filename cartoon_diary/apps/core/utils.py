"""Helper utilities used across apps."""

from __future__ import annotations

from datetime import date, timedelta


def get_month_bounds(target: date) -> tuple[date, date]:
    """Return first and last day for the month of the given date."""

    start = target.replace(day=1)
    if target.month == 12:
        next_month = target.replace(year=target.year + 1, month=1, day=1)
    else:
        next_month = target.replace(month=target.month + 1, day=1)
    end = next_month - timedelta(days=1)
    return start, end
