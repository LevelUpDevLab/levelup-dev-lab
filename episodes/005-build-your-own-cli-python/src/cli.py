"""Episode 005 — build your own CLI: a tiny wordcount tool."""

import argparse
import sys
from collections import namedtuple
from typing import List, Optional

Counts = namedtuple("Counts", ["lines", "words", "chars"])


def count(text: str) -> Counts:
    """Return line/word/char counts for a block of text. Pure and testable."""
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    words = len(text.split())
    chars = len(text)
    return Counts(lines=lines, words=words, chars=chars)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Count lines, words, and characters (file or stdin).",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File to read. Omit to read from stdin.",
    )
    parser.add_argument("-l", "--lines", action="store_true", help="show line count")
    parser.add_argument("-w", "--words", action="store_true", help="show word count")
    parser.add_argument("-c", "--chars", action="store_true", help="show char count")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    text = open(args.path, encoding="utf-8").read() if args.path else sys.stdin.read()
    result = count(text)

    # If no flag is given, show everything.
    show_all = not (args.lines or args.words or args.chars)
    parts = []
    if show_all or args.lines:
        parts.append(str(result.lines))
    if show_all or args.words:
        parts.append(str(result.words))
    if show_all or args.chars:
        parts.append(str(result.chars))
    print("\t".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
