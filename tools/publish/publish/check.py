"""``publish check`` — validate an episode folder before publishing."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import REQUIRED_README_SECTIONS, PublishError

TODO_MARKERS = ("TODO", "FIXME", "_TODO_")
_TEXT_SUFFIXES = {".md", ".py", ".js", ".ts", ".java", ".txt", ".yml", ".yaml"}
_SKIP_PARTS = {".venv", "__pycache__", "node_modules", ".git"}


@dataclass
class CheckResult:
    """One validation line: did it pass, and any detail to show."""

    name: str
    ok: bool
    detail: str = ""


def find_missing_sections(readme_text: str) -> list[str]:
    """Return required README sections whose heading is absent."""
    headings = [
        line.lstrip("#").strip().lower()
        for line in readme_text.splitlines()
        if line.lstrip().startswith("#")
    ]
    return [
        section
        for section in REQUIRED_README_SECTIONS
        if not any(section.lower() in heading for heading in headings)
    ]


def find_todos(episode: Path) -> list[str]:
    """Return ``path:line`` locations of any leftover TODO/FIXME markers."""
    hits: list[str] = []
    for path in sorted(episode.rglob("*")):
        if not path.is_file() or path.suffix not in _TEXT_SUFFIXES:
            continue
        if _SKIP_PARTS.intersection(path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(lines, 1):
            if any(marker in line for marker in TODO_MARKERS):
                hits.append(f"{path.relative_to(episode)}:{lineno}")
    return hits


def _run_make(episode: Path, target: str, timeout: int) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["make", target],
            cwd=episode,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, "make not found on PATH"
    except subprocess.TimeoutExpired:
        return False, f"`make {target}` timed out after {timeout}s"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()[-3:]
        return False, f"`make {target}` exited {proc.returncode}: " + " / ".join(tail)
    return True, ""


def check_episode(
    episode: Path,
    *,
    run_code: bool = True,
    setup: bool = True,
    timeout: int = 300,
) -> list[CheckResult]:
    """Validate *episode* and return one CheckResult per criterion."""
    if not episode.is_dir():
        raise PublishError(f"Episode folder not found: {episode}")

    results: list[CheckResult] = []

    readme = episode / "README.md"
    if not readme.is_file():
        results.append(CheckResult("README.md exists", False, "missing"))
    else:
        results.append(CheckResult("README.md exists", True))
        missing = find_missing_sections(readme.read_text(encoding="utf-8"))
        results.append(
            CheckResult(
                "README sections",
                not missing,
                "" if not missing else "missing: " + ", ".join(missing),
            )
        )

    results.append(
        CheckResult("walkthrough.md exists", (episode / "walkthrough.md").is_file())
    )

    todos = find_todos(episode)
    results.append(
        CheckResult(
            "no TODOs left",
            not todos,
            "" if not todos else f"{len(todos)} found (e.g. {todos[0]})",
        )
    )

    if run_code:
        if setup:
            # Best effort: any real failure resurfaces in run/test below.
            _run_make(episode, "setup", timeout)
        run_ok, run_detail = _run_make(episode, "run", timeout)
        results.append(CheckResult("code runs (make run)", run_ok, run_detail))
        test_ok, test_detail = _run_make(episode, "test", timeout)
        results.append(CheckResult("tests pass (make test)", test_ok, test_detail))

    return results
