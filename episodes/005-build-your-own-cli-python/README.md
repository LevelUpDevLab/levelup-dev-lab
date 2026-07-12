# 005 — Build Your Own CLI (Python)

> Pillar: _Build Your Own Tooling_ · Language(s): _Python_

## Summary

Build a small but real command-line tool with `argparse`: a `wordcount` CLI that
counts lines, words, and characters from a file or stdin. This is your first step
from _using_ tools to _building_ them.

## What you'll learn

- Structuring a CLI with `argparse` (subcommand-free, flags, positional args).
- Reading from a file **or** stdin so your tool composes in a pipeline.
- Keeping the core logic in a pure function so it's testable.

## Prereqs

- Python 3.9+
- `make`

## Run it

```bash
make setup             # create a virtualenv
make run               # runs the CLI against a sample string
echo "hello there" | python src/cli.py    # or pipe your own input
python src/cli.py README.md --words        # count words in a file
make test              # runs the sanity test
```

## Code walkthrough

- [`src/cli.py`](src/cli.py) — `count(text)` returns a `Counts` namedtuple (pure,
  testable). `main(argv)` wires up `argparse`, reads from the given file or stdin,
  and prints the requested counts.
- [`tests/test_cli.py`](tests/test_cli.py) — checks `count()` on a known string.

## Try it yourself

- Add a `--lines` / `--chars` combo and default to printing all three.
- Add a `--top N` flag that prints the N most common words.

## Links

- 📺 Video: _TODO_
- 📄 Prev: [004 — Observability Basics](../004-observability-basics/)
- 📄 Next: [006 — Build Your Own CLI (Node)](../006-build-your-own-cli-node/)
