"""Shared paths, constants, and lookup helpers for the publish tool."""

import re
import subprocess
from pathlib import Path

# README sections every episode must have before it can be published.
REQUIRED_README_SECTIONS = (
    "Summary",
    "What you'll learn",
    "Prereqs",
    "Run it",
    "Code walkthrough",
    "Try it yourself",
    "Links",
)

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NUMBERED_SLUG_RE = re.compile(r"^(\d{3})-(.+)$")


class PublishError(Exception):
    """A user-facing, recoverable error (bad slug, missing episode, etc.)."""


def episodes_dir(repo_root: Path) -> Path:
    return repo_root / "episodes"


def template_path(repo_root: Path) -> Path:
    return repo_root / "shared" / "templates" / "episode-readme.md"


def resolve_repo_root(explicit: Path | None = None) -> Path:
    """Locate the repo root.

    Order of preference: an explicit path, then ``git rev-parse`` (works from
    anywhere inside the checkout), then walking up from this file looking for
    the ``episodes/`` + ``shared/`` markers.
    """
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not episodes_dir(root).is_dir():
            raise PublishError(f"No episodes/ directory under {root}")
        return root

    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        candidate = Path(out.stdout.strip())
        if episodes_dir(candidate).is_dir():
            return candidate
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    for parent in Path(__file__).resolve().parents:
        if episodes_dir(parent).is_dir() and (parent / "shared").is_dir():
            return parent

    raise PublishError(
        "Could not locate the repo root. Pass --repo or run inside the repo."
    )


def resolve_episode(repo_root: Path, slug: str) -> Path:
    """Resolve a user-supplied slug to an existing episode directory.

    Accepts the full folder name (``001-automation-hello-world``), the numeric
    prefix (``001`` or ``1``), or the descriptive part
    (``automation-hello-world``). Raises on no match or an ambiguous one.
    """
    eps = episodes_dir(repo_root)
    if not eps.is_dir():
        raise PublishError(f"No episodes/ directory under {repo_root}")

    exact = eps / slug
    if exact.is_dir():
        return exact

    matches: list[Path] = []
    for folder in sorted(p for p in eps.iterdir() if p.is_dir()):
        m = NUMBERED_SLUG_RE.match(folder.name)
        number, descriptive = (m.group(1), m.group(2)) if m else ("", folder.name)
        keys = {folder.name, descriptive}
        if number:
            keys |= {number, number.lstrip("0")}
        if slug in keys:
            matches.append(folder)

    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise PublishError(f"No episode matches '{slug}' under {eps}")
    names = ", ".join(p.name for p in matches)
    raise PublishError(f"'{slug}' is ambiguous — matches: {names}")
