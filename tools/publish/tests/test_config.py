"""Tests for path/slug resolution."""

import pytest

from publish.config import PublishError, resolve_episode, resolve_repo_root


def test_resolve_repo_root_explicit(repo):
    assert resolve_repo_root(repo) == repo


def test_resolve_repo_root_rejects_non_repo(tmp_path):
    with pytest.raises(PublishError):
        resolve_repo_root(tmp_path)


def test_resolve_episode_by_full_name(make_episode, repo):
    make_episode("001-automation-hello-world")
    got = resolve_episode(repo, "001-automation-hello-world")
    assert got.name == "001-automation-hello-world"


def test_resolve_episode_by_number(make_episode, repo):
    make_episode("001-automation-hello-world")
    assert resolve_episode(repo, "001").name == "001-automation-hello-world"
    assert resolve_episode(repo, "1").name == "001-automation-hello-world"


def test_resolve_episode_by_descriptive_slug(make_episode, repo):
    make_episode("001-automation-hello-world")
    got = resolve_episode(repo, "automation-hello-world")
    assert got.name == "001-automation-hello-world"


def test_resolve_episode_missing(repo):
    with pytest.raises(PublishError, match="No episode matches"):
        resolve_episode(repo, "nope")
