"""Walk a folder and collect the metadata the report needs."""

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class AutomationError(Exception):
    """A user-facing, recoverable failure (bad input path, etc.)."""


@dataclass(frozen=True)
class FileEntry:
    """One scanned file and the three facts the report cares about."""

    name: str
    extension: str  # lowercase, without the dot; "" when there is none
    size_bytes: int
    modified: datetime


def scan_folder(folder: Path) -> list[FileEntry]:
    """Return metadata for every file directly inside *folder*.

    This is a flat scan: subdirectories are skipped, not descended into.
    Raises :class:`AutomationError` if the path is missing or is not a folder.
    """
    if not folder.exists():
        raise AutomationError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise AutomationError(f"Not a folder: {folder}")

    entries: list[FileEntry] = []
    for child in sorted(folder.iterdir()):
        if not child.is_file():
            logger.debug("skipping non-file: %s", child.name)
            continue
        try:
            stat = child.stat()
        except OSError as exc:  # pragma: no cover - e.g. a broken symlink
            logger.warning("could not read %s: %s", child.name, exc)
            continue
        entries.append(
            FileEntry(
                name=child.name,
                extension=child.suffix.lower().lstrip("."),
                size_bytes=stat.st_size,
                modified=datetime.fromtimestamp(stat.st_mtime),
            )
        )

    logger.info("scanned %d file(s) in %s", len(entries), folder)
    return entries
