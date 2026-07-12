"""Tests for `publish check` validation."""

import pytest

from publish.check import check_episode, find_missing_sections, find_todos
from publish.config import PublishError


def _by_name(results):
    return {r.name: r for r in results}


def test_find_missing_sections_all_present():
    text = "\n".join(
        f"## {s}"
        for s in [
            "Summary",
            "What you'll learn",
            "Prereqs",
            "Run it",
            "Code walkthrough",
            "Try it yourself",
            "Links",
        ]
    )
    assert find_missing_sections(text) == []


def test_find_missing_sections_reports_gaps():
    missing = find_missing_sections("## Summary\n## Links\n")
    assert "Prereqs" in missing
    assert "Summary" not in missing


def test_find_todos(make_episode):
    episode = make_episode(todos=True)
    hits = find_todos(episode)
    assert any("main.py" in h for h in hits)


def test_check_happy_path(make_episode):
    episode = make_episode(makefile="ok")
    results = _by_name(check_episode(episode))
    assert results["README sections"].ok
    assert results["walkthrough.md exists"].ok
    assert results["no TODOs left"].ok
    assert results["code runs (make run)"].ok
    assert results["tests pass (make test)"].ok


def test_check_flags_failing_tests(make_episode):
    episode = make_episode(makefile="fail_test")
    results = _by_name(check_episode(episode))
    assert results["tests pass (make test)"].ok is False


def test_check_flags_todos_and_missing_walkthrough(make_episode):
    episode = make_episode(walkthrough=False, todos=True)
    results = _by_name(check_episode(episode, run_code=False))
    assert results["walkthrough.md exists"].ok is False
    assert results["no TODOs left"].ok is False


def test_check_missing_episode(repo):
    with pytest.raises(PublishError):
        check_episode(repo / "episodes" / "ghost")


def test_check_no_run_skips_make(make_episode):
    episode = make_episode(makefile="none")
    names = {r.name for r in check_episode(episode, run_code=False)}
    assert "code runs (make run)" not in names
