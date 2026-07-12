"""Sanity test for episode 002 (Python)."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "python"))

from overdue import days_overdue  # noqa: E402


def test_late():
    assert days_overdue(date(2026, 7, 1), date(2026, 7, 12)) == 11


def test_on_time_is_zero():
    assert days_overdue(date(2026, 7, 12), date(2026, 7, 1)) == 0
