"""``publish shorts`` — pull [SHORT] segments out of an episode script.

A script marks candidate Shorts inline::

    [SHORT: Why naming matters]
    spoken content, a sentence or three...
    [/SHORT]

The title after the colon is optional. Each block becomes a file under
``shorts/``, with an estimated spoken duration so you can see at a glance
whether it lands in the 60–90 second window.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from .config import PublishError

_SHORT_RE = re.compile(
    r"\[SHORT(?::\s*(?P<title>[^\]]+))?\]\s*\n(?P<body>.*?)\n?\[/SHORT\]",
    re.DOTALL,
)

# A relaxed speaking rate; good enough to flag segments that are too long/short.
WORDS_PER_SECOND = 2.5
MIN_SECONDS = 60
MAX_SECONDS = 90
_SCRIPT_NAMES = ("script.md", "SCRIPT.md", "episode-script.md")


@dataclass
class ShortSegment:
    """One extracted [SHORT] block plus its duration estimate."""

    index: int
    title: str
    body: str
    word_count: int
    est_seconds: float
    in_range: bool


def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "short"


def find_script(episode: Path) -> Path:
    """Return the episode's script file, or raise if none is present."""
    for name in _SCRIPT_NAMES:
        candidate = episode / name
        if candidate.is_file():
            return candidate
    raise PublishError(
        f"No episode script in {episode} (looked for {', '.join(_SCRIPT_NAMES)})."
    )


def extract_shorts(script_text: str) -> list[ShortSegment]:
    """Parse every [SHORT]…[/SHORT] block into a ShortSegment."""
    segments: list[ShortSegment] = []
    for index, match in enumerate(_SHORT_RE.finditer(script_text), 1):
        body = match.group("body").strip()
        title = (match.group("title") or f"Short {index}").strip()
        words = len(body.split())
        seconds = words / WORDS_PER_SECOND
        segments.append(
            ShortSegment(
                index=index,
                title=title,
                body=body,
                word_count=words,
                est_seconds=seconds,
                in_range=MIN_SECONDS <= seconds <= MAX_SECONDS,
            )
        )
    return segments


def render_short(segment: ShortSegment, episode_name: str) -> str:
    """Render one segment as a standalone Markdown file body."""
    status = "in range" if segment.in_range else "OUT of 60–90s range"
    return (
        f"# Short {segment.index:02d} — {segment.title}\n\n"
        f"- Episode: {episode_name}\n"
        f"- Estimated length: {segment.est_seconds:.0f}s ({status})\n"
        f"- Word count: {segment.word_count}\n\n"
        f"## Script\n\n{segment.body}\n"
    )


def write_shorts(episode: Path, segments: list[ShortSegment]) -> list[Path]:
    """Write each segment to ``shorts/short-NN-title.md`` and return the paths."""
    out_dir = episode / "shorts"
    out_dir.mkdir(exist_ok=True)
    written: list[Path] = []
    for segment in segments:
        path = out_dir / f"short-{segment.index:02d}-{_slugify(segment.title)}.md"
        path.write_text(render_short(segment, episode.name), encoding="utf-8")
        written.append(path)
    return written
