"""Tests for `publish new` scaffolding."""

import pytest

from publish.config import PublishError
from publish.scaffold import (
    next_episode_number,
    scaffold_episode,
    title_from_slug,
)


def test_title_from_slug():
    assert title_from_slug("automation-file-watcher") == "Automation File Watcher"


def test_next_episode_number(make_episode, repo):
    assert next_episode_number(repo) == 1
    make_episode("001-demo")
    make_episode("004-other")
    assert next_episode_number(repo) == 5


def test_scaffold_creates_full_layout(repo):
    episode = scaffold_episode(repo, "file-watcher")
    assert episode.name == "001-file-watcher"
    for rel in [
        "README.md",
        "walkthrough.md",
        "Makefile",
        "src/main.py",
        "tests/test_smoke.py",
    ]:
        assert (episode / rel).is_file(), rel
    readme = (episode / "README.md").read_text(encoding="utf-8")
    assert readme.startswith("# 001 — File Watcher")


def test_scaffold_honors_number_prefix_in_slug(repo):
    episode = scaffold_episode(repo, "007-cool-thing")
    assert episode.name == "007-cool-thing"


def test_scaffold_explicit_number_option(repo):
    episode = scaffold_episode(repo, "cool-thing", number=9)
    assert episode.name == "009-cool-thing"


def test_scaffold_rejects_bad_slug(repo):
    with pytest.raises(PublishError, match="Invalid slug"):
        scaffold_episode(repo, "Bad Slug!")


def test_scaffold_rejects_duplicate(repo):
    scaffold_episode(repo, "dup", number=1)
    with pytest.raises(PublishError, match="already exists"):
        scaffold_episode(repo, "dup", number=1)
