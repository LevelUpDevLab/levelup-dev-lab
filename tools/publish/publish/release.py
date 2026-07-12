"""``publish release`` — tag the episode, build release notes, print a checklist."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import NUMBERED_SLUG_RE, PublishError

YOUTUBE_CHECKLIST = (
    "Title: front-load the keyword; keep it under ~60 characters.",
    "Description: paste the release notes; add chapters, links, and the repo URL.",
    "Thumbnail: upload the custom thumbnail (1280x720, readable when small).",
    "End screen: add subscribe + next-episode elements in the last 20 seconds.",
    "Cards: link the related episode(s) and the GitHub repo.",
    "Playlist: add the video to its season / pillar playlist.",
    "Visibility: set Unlisted for review, then Public when ready.",
)


@dataclass
class ReleaseInfo:
    """The computed tag name, episode title, and generated release notes."""

    tag: str
    title: str
    notes: str


def extract_section(readme_text: str, name: str) -> str:
    """Return the body under a ``## name`` heading, up to the next heading."""
    out: list[str] = []
    capturing = False
    for line in readme_text.splitlines():
        if line.lstrip().startswith("#"):
            if capturing:
                break
            capturing = name.lower() in line.lstrip("#").strip().lower()
            continue
        if capturing:
            out.append(line)
    return "\n".join(out).strip()


def episode_title(readme_text: str, fallback: str) -> str:
    for line in readme_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_release(episode: Path) -> ReleaseInfo:
    """Compute the tag and render release notes from the episode README."""
    readme_path = episode / "README.md"
    if not readme_path.is_file():
        raise PublishError(f"README.md not found in {episode}")
    readme = readme_path.read_text(encoding="utf-8")

    m = NUMBERED_SLUG_RE.match(episode.name)
    if not m:
        raise PublishError(f"Episode folder '{episode.name}' is not NNN-slug form")
    tag = f"ep-{m.group(1)}"

    title = episode_title(readme, episode.name)
    summary = extract_section(readme, "Summary") or "_No summary provided._"
    learn = extract_section(readme, "What you'll learn")

    notes = f"# {title}\n\n{summary}\n"
    if learn:
        notes += f"\n## What you'll learn\n\n{learn}\n"
    notes += f"\nEpisode code: `episodes/{episode.name}/`\n"
    return ReleaseInfo(tag=tag, title=title, notes=notes)


def tag_exists(repo_root: Path, tag: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "tag", "--list", tag],
        capture_output=True,
        text=True,
    )
    return bool(proc.stdout.strip())


def create_tag(repo_root: Path, tag: str, message: str) -> None:
    """Create an annotated git tag. Raises if it already exists or git fails."""
    if tag_exists(repo_root, tag):
        raise PublishError(f"Tag already exists: {tag}")
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "tag", "-a", tag, "-m", message],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise PublishError(f"git tag failed: {proc.stderr.strip()}")


def render_checklist(info: ReleaseInfo, episode_name: str) -> str:
    header = f"Manual YouTube Studio steps for {episode_name} ({info.tag}):"
    lines = [header, ""] + [f"  [ ] {item}" for item in YOUTUBE_CHECKLIST]
    return "\n".join(lines)
