"""Tests for `publish release` notes + tagging."""

import pytest

from publish.config import PublishError
from publish.release import (
    build_release,
    create_tag,
    extract_section,
    render_checklist,
    tag_exists,
)


def test_extract_section():
    readme = "# T\n\n## Summary\n\nHello there.\n\n## Links\n\n- x\n"
    assert extract_section(readme, "Summary") == "Hello there."
    assert extract_section(readme, "Nope") == ""


def test_build_release_from_readme(make_episode):
    episode = make_episode("003-demo")
    info = build_release(episode)
    assert info.tag == "ep-003"
    assert info.title == "001 — Demo"  # from the README H1
    assert "A demo episode." in info.notes
    assert "What you'll learn" in info.notes
    assert "episodes/003-demo/" in info.notes


def test_build_release_requires_readme(make_episode):
    episode = make_episode("003-demo", readme=False)
    with pytest.raises(PublishError, match="README.md not found"):
        build_release(episode)


def test_render_checklist_mentions_youtube_steps(make_episode):
    info = build_release(make_episode("003-demo"))
    checklist = render_checklist(info, "003-demo")
    for keyword in ["Title", "Description", "Thumbnail", "End screen", "Cards"]:
        assert keyword in checklist


def test_create_tag_and_exists(make_episode, git_repo):
    info = build_release(make_episode("003-demo"))
    assert tag_exists(git_repo, info.tag) is False
    create_tag(git_repo, info.tag, info.notes)
    assert tag_exists(git_repo, info.tag) is True


def test_create_tag_rejects_duplicate(make_episode, git_repo):
    info = build_release(make_episode("003-demo"))
    create_tag(git_repo, info.tag, info.notes)
    with pytest.raises(PublishError, match="already exists"):
        create_tag(git_repo, info.tag, info.notes)
