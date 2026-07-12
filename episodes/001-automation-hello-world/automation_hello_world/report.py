"""Turn a list of :class:`FileEntry` objects into a Markdown report."""

import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from .scanner import FileEntry

logger = logging.getLogger(__name__)

_UNITS = ("B", "KB", "MB", "GB", "TB")


def human_size(num_bytes: int) -> str:
    """Format a byte count as a short human-readable string (e.g. ``1.5 KB``)."""
    size = float(num_bytes)
    for unit in _UNITS:
        if size < 1024 or unit == _UNITS[-1]:
            precision = 0 if unit == "B" else 1
            return f"{size:.{precision}f} {unit}"
        size /= 1024
    # Unreachable (the loop always returns), but keeps type checkers happy.
    return f"{size:.1f} {_UNITS[-1]}"


def build_report(
    folder: Path,
    entries: list[FileEntry],
    *,
    now: datetime | None = None,
) -> str:
    """Build the full Markdown report for *entries* found in *folder*.

    *now* is injectable so tests can pin the "Generated" timestamp.
    """
    generated = (now or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        f"# File report for `{folder}`",
        "",
        f"_Generated {generated}_",
        "",
    ]

    if not entries:
        lines += ["No files found in this folder.", ""]
        return "\n".join(lines)

    total_size = sum(entry.size_bytes for entry in entries)
    lines += [
        f"- **Files:** {len(entries)}",
        f"- **Total size:** {human_size(total_size)}",
        "",
    ]

    # Group the files by extension once; both sections below reuse it.
    groups: dict[str, list[FileEntry]] = defaultdict(list)
    for entry in entries:
        groups[entry.extension].append(entry)

    # Summary table, most-populous extension first.
    lines += [
        "## Summary by extension",
        "",
        "| Extension | Files | Size |",
        "| --- | ---: | ---: |",
    ]
    for ext in sorted(groups, key=lambda e: (-len(groups[e]), e)):
        label = f"`.{ext}`" if ext else "_(none)_"
        group_size = human_size(sum(item.size_bytes for item in groups[ext]))
        lines.append(f"| {label} | {len(groups[ext])} | {group_size} |")
    lines.append("")

    # Per-extension detail, alphabetical, with each file's size + mtime.
    lines += ["## Files by extension", ""]
    for ext in sorted(groups):
        heading = f".{ext}" if ext else "(no extension)"
        lines += [
            f"### {heading}",
            "",
            "| File | Size | Last modified |",
            "| --- | ---: | --- |",
        ]
        for entry in sorted(groups[ext], key=lambda item: item.name):
            modified = entry.modified.strftime("%Y-%m-%d %H:%M")
            lines.append(
                f"| {entry.name} | {human_size(entry.size_bytes)} | {modified} |"
            )
        lines.append("")

    logger.debug("built report with %d extension group(s)", len(groups))
    return "\n".join(lines)
