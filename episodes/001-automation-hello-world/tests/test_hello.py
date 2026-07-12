"""Sanity test for episode 001."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from hello import greet  # noqa: E402


def test_greet_default():
    assert greet() == "Hello, World! Welcome to LevelUp Dev Lab."


def test_greet_name():
    assert "Ada" in greet("Ada")
