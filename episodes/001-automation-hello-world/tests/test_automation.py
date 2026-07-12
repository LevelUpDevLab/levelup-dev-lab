"""Tests for episode 001's folder-report automation."""

from datetime import datetime
from pathlib import Path

import pytest

from automation_hello_world.cli import main
from automation_hello_world.report import build_report, human_size
from automation_hello_world.scanner import AutomationError, scan_folder


def _make_sample_files(folder: Path) -> None:
    (folder / "notes.txt").write_text("hello", encoding="utf-8")
    (folder / "data.csv").write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    (folder / "script.py").write_text("print('hi')\n", encoding="utf-8")
    (folder / "README").write_text("no extension here", encoding="utf-8")


def test_happy_path(tmp_path):
    """A folder with mixed files produces a grouped report and exit code 0."""
    _make_sample_files(tmp_path)
    output = tmp_path / "report.md"

    exit_code = main([str(tmp_path), "-o", str(output)])

    assert exit_code == 0
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "**Files:** 4" in text
    assert "`.py`" in text
    assert "_(none)_" in text  # the extension-less README
    assert "notes.txt" in text


def test_empty_folder(tmp_path):
    """An empty folder still succeeds and writes a 'no files' report."""
    output = tmp_path / "report.md"

    exit_code = main([str(tmp_path), "-o", str(output)])

    assert exit_code == 0
    assert "No files found" in output.read_text(encoding="utf-8")


def test_missing_folder(tmp_path):
    """A folder that does not exist fails with a non-zero exit and no output."""
    missing = tmp_path / "does-not-exist"
    output = tmp_path / "report.md"

    exit_code = main([str(missing), "-o", str(output)])

    assert exit_code == 2
    assert not output.exists()  # nothing is written when the scan fails


def test_scan_folder_raises_on_missing(tmp_path):
    """scan_folder surfaces a clear AutomationError for a missing path."""
    with pytest.raises(AutomationError, match="does not exist"):
        scan_folder(tmp_path / "nope")


def test_human_size_formats_units():
    assert human_size(0) == "0 B"
    assert human_size(512) == "512 B"
    assert human_size(1536) == "1.5 KB"


def test_report_timestamp_is_injectable(tmp_path):
    """build_report uses the injected 'now', which keeps output deterministic."""
    pinned = datetime(2026, 1, 2, 3, 4, 5)
    report = build_report(tmp_path, [], now=pinned)
    assert "_Generated 2026-01-02 03:04:05_" in report
