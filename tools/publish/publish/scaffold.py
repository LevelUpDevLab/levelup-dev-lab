"""``publish new`` — scaffold a new episode folder from the shared template."""

from pathlib import Path

from .config import (
    NUMBERED_SLUG_RE,
    SLUG_RE,
    PublishError,
    episodes_dir,
    template_path,
)

_WALKTHROUGH_STUB = """# Walkthrough — {title}

The narration track: one short paragraph per function, in the order you'd
explain it on camera.

TODO: write the walkthrough once the code is in place.
"""

_MAIN_STUB = '''"""Episode source — replace this stub with the real thing."""


def main() -> None:
    print("Hello from this episode. Replace me.")


if __name__ == "__main__":
    main()
'''

_TEST_STUB = '''"""Sanity test for this episode."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import main  # noqa: E402


def test_main_runs(capsys):
    main()
    assert capsys.readouterr().out.strip()
'''

_MAKEFILE = (
    "PY := python3\n"
    "VENV := .venv\n"
    "BIN := $(VENV)/bin\n"
    "\n"
    ".PHONY: setup run test clean\n"
    "\n"
    "setup:\n"
    "\t$(PY) -m venv $(VENV)\n"
    "\t$(BIN)/pip install --quiet --upgrade pip pytest\n"
    "\n"
    "run:\n"
    "\t$(PY) src/main.py\n"
    "\n"
    "test:\n"
    '\t@if [ -x "$(BIN)/pytest" ]; then $(BIN)/pytest -q tests; '
    "else $(PY) -m pytest -q tests; fi\n"
    "\n"
    "clean:\n"
    "\trm -rf $(VENV) .pytest_cache tests/__pycache__ src/__pycache__\n"
)


def next_episode_number(repo_root: Path) -> int:
    """Return the next episode number (highest existing + 1, or 1)."""
    highest = 0
    eps = episodes_dir(repo_root)
    if eps.is_dir():
        for folder in eps.iterdir():
            m = NUMBERED_SLUG_RE.match(folder.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def title_from_slug(slug: str) -> str:
    """Turn ``automation-file-watcher`` into ``Automation File Watcher``."""
    return slug.replace("-", " ").title()


def scaffold_episode(repo_root: Path, slug: str, number: int | None = None) -> Path:
    """Create ``episodes/NNN-slug`` from the template and return its path.

    *slug* may be a bare descriptive slug (``automation-file-watcher``) or
    already carry a number (``007-automation-file-watcher``). An explicit
    *number* wins only when the slug has none.
    """
    m = NUMBERED_SLUG_RE.match(slug)
    if m:
        number = int(m.group(1))
        descriptive = m.group(2)
    else:
        descriptive = slug

    if not SLUG_RE.match(descriptive):
        raise PublishError(f"Invalid slug '{descriptive}': use lowercase-with-hyphens.")

    if number is None:
        number = next_episode_number(repo_root)

    episode = episodes_dir(repo_root) / f"{number:03d}-{descriptive}"
    if episode.exists():
        raise PublishError(f"Episode already exists: {episode}")

    template = template_path(repo_root)
    if not template.is_file():
        raise PublishError(f"Template not found: {template}")

    (episode / "src").mkdir(parents=True)
    (episode / "tests").mkdir()

    readme = (
        template.read_text(encoding="utf-8")
        .replace("{{NUMBER}}", f"{number:03d}")
        .replace("{{TITLE}}", title_from_slug(descriptive))
        .replace("{{PILLAR}}", "TODO")
        .replace("{{LANGUAGES}}", "Python")
    )
    (episode / "README.md").write_text(readme, encoding="utf-8")
    (episode / "walkthrough.md").write_text(
        _WALKTHROUGH_STUB.format(title=title_from_slug(descriptive)),
        encoding="utf-8",
    )
    (episode / "Makefile").write_text(_MAKEFILE, encoding="utf-8")
    (episode / "src" / "main.py").write_text(_MAIN_STUB, encoding="utf-8")
    (episode / "tests" / "test_smoke.py").write_text(_TEST_STUB, encoding="utf-8")
    return episode
