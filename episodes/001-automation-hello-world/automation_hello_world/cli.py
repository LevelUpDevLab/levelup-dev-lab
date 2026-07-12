"""Command-line entry point: scan a folder and write a Markdown report."""

import argparse
import logging
from pathlib import Path

from . import __version__
from .report import build_report
from .scanner import AutomationError, scan_folder

logger = logging.getLogger("automation_hello_world")

DEFAULT_OUTPUT = Path("report.md")


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser (kept separate so it is easy to test)."""
    parser = argparse.ArgumentParser(
        prog="automation_hello_world",
        description=(
            "Scan a folder of mixed files and write a Markdown status report "
            "that groups files by extension, with each file's size and "
            "last-modified date."
        ),
        epilog="Example: python -m automation_hello_world ./Downloads -o downloads.md",
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="folder whose top-level files should be reported on",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="where to write the report (default: ./report.md)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase logging detail (-v enables debug logging)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def configure_logging(verbosity: int) -> None:
    """Map the -v count to a logging level and send logs to stderr."""
    level = logging.DEBUG if verbosity else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main(argv: list[str] | None = None) -> int:
    """Run the tool. Returns a process exit code (0 = success, non-zero = failure)."""
    args = build_parser().parse_args(argv)
    configure_logging(args.verbose)

    try:
        entries = scan_folder(args.folder)
    except AutomationError as exc:
        logger.error("%s", exc)
        return 2

    report = build_report(args.folder, entries)
    try:
        args.output.write_text(report.rstrip("\n") + "\n", encoding="utf-8")
    except OSError as exc:
        logger.error("could not write %s: %s", args.output, exc)
        return 2

    logger.info("wrote %s (%d file(s))", args.output, len(entries))
    return 0
