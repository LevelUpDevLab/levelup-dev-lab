"""Tests for `publish shorts` extraction."""

import pytest

from publish.config import PublishError
from publish.shorts import extract_shorts, find_script, write_shorts

_SCRIPT = """Intro chatter that is not a short.

[SHORT: Why naming matters]
A good name is the cheapest documentation you will ever write.
It saves the next reader from guessing.
[/SHORT]

Some connective narration here.

[SHORT]
Tests are not about proving correctness. They are about changing code
without fear later.
[/SHORT]
"""


def test_extract_finds_blocks_with_and_without_titles():
    segments = extract_shorts(_SCRIPT)
    assert len(segments) == 2
    assert segments[0].title == "Why naming matters"
    assert segments[1].title == "Short 2"  # default when untitled
    assert "connective narration" not in segments[0].body


def test_extract_estimates_duration():
    segments = extract_shorts(_SCRIPT)
    # ~2.5 words/sec; the sample blocks are short, so out of the 60-90s range.
    assert segments[0].word_count > 0
    assert segments[0].in_range is False


def test_extract_returns_empty_when_no_blocks():
    assert extract_shorts("just prose, no markers") == []


def test_write_shorts_creates_files(make_episode):
    episode = make_episode()
    segments = extract_shorts(_SCRIPT)
    written = write_shorts(episode, segments)
    assert len(written) == 2
    assert (episode / "shorts").is_dir()
    first = written[0].read_text(encoding="utf-8")
    assert "# Short 01 — Why naming matters" in first
    assert "Estimated length" in first


def test_find_script_missing(make_episode):
    episode = make_episode()
    with pytest.raises(PublishError, match="No episode script"):
        find_script(episode)


def test_find_script_present(make_episode):
    episode = make_episode()
    (episode / "script.md").write_text(_SCRIPT, encoding="utf-8")
    assert find_script(episode).name == "script.md"
