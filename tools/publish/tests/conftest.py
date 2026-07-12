"""Shared fixtures: a throwaway repo with an episodes/ tree and template."""

import subprocess

import pytest

_TEMPLATE = """# {{NUMBER}} — {{TITLE}}

> Pillar: _{{PILLAR}}_ · Language(s): _{{LANGUAGES}}_

## Summary

_Summary._

## What you'll learn

- _Thing._

## Prereqs

- _Python._

## Run it

_Run._

## Code walkthrough

_Walk._

## Try it yourself

- _Try._

## Links

- _Link._
"""

# A Makefile whose targets all succeed instantly (no venv, no network).
_MAKEFILE_OK = (
    ".PHONY: setup run test\n"
    "setup:\n\t@true\n"
    "run:\n\t@echo running\n"
    "test:\n\t@echo testing\n"
)

# Same, but `make test` fails.
_MAKEFILE_FAIL_TEST = (
    ".PHONY: setup run test\n"
    "setup:\n\t@true\n"
    "run:\n\t@echo running\n"
    "test:\n\t@echo boom; exit 1\n"
)

_README_OK = """# 001 — Demo

## Summary

A demo episode.

## What you'll learn

- How the tool works.

## Prereqs

- Python.

## Run it

`make run`

## Code walkthrough

Some words.

## Try it yourself

- Extend it.

## Links

- Somewhere.
"""


@pytest.fixture
def repo(tmp_path):
    """A minimal repo root: episodes/ plus shared/templates/episode-readme.md."""
    (tmp_path / "episodes").mkdir()
    templates = tmp_path / "shared" / "templates"
    templates.mkdir(parents=True)
    (templates / "episode-readme.md").write_text(_TEMPLATE, encoding="utf-8")
    return tmp_path


@pytest.fixture
def make_episode(repo):
    """Factory: build an episode folder with tunable defects for check tests."""

    def _make(
        name="001-demo",
        *,
        readme=True,
        walkthrough=True,
        todos=False,
        makefile="ok",
    ):
        episode = repo / "episodes" / name
        (episode / "src").mkdir(parents=True)
        (episode / "tests").mkdir()
        if readme:
            (episode / "README.md").write_text(_README_OK, encoding="utf-8")
        if walkthrough:
            (episode / "walkthrough.md").write_text("# Walkthrough\n", encoding="utf-8")
        if todos:
            (episode / "src" / "main.py").write_text(
                "# TODO: finish this\n", encoding="utf-8"
            )
        makefiles = {"ok": _MAKEFILE_OK, "fail_test": _MAKEFILE_FAIL_TEST}
        if makefile in makefiles:
            (episode / "Makefile").write_text(makefiles[makefile], encoding="utf-8")
        return episode

    return _make


@pytest.fixture
def git_repo(repo):
    """The repo fixture, initialized as a git repo with one commit."""
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.email", "t@example.com"], cwd=repo, check=True
    )
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "init"],
        cwd=repo,
        check=True,
    )
    return repo
