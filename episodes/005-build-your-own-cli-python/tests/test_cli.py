"""Sanity test for episode 005."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cli import count  # noqa: E402


def test_count_basic():
    c = count("hello there\nfriend\n")
    assert c.lines == 2
    assert c.words == 3
    assert c.chars == len("hello there\nfriend\n")


def test_count_no_trailing_newline():
    assert count("one two").lines == 1
