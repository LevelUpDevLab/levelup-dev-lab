"""Sanity test for episode 004."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from observe import sum_of_squares, timed  # noqa: E402


def test_sum_of_squares():
    assert sum_of_squares(4) == 0 + 1 + 4 + 9


def test_timed_records_duration():
    with timed("noop") as t:
        pass
    assert t["seconds"] >= 0
