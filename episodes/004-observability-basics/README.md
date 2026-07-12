# 004 — Observability Basics

> Pillar: _Best Practices_ · Language(s): _Python_

## Summary

Stop debugging with `print()`. This episode swaps ad-hoc prints for structured
logging and a tiny timing helper, so your program can _tell you_ what it's doing
and how long it took.

## What you'll learn

- The difference between `print` and the `logging` module (levels, timestamps, config).
- Emitting structured, greppable log lines.
- A reusable `timed` context manager to measure a block of work.

## Prereqs

- Python 3.9+
- `make`

## Run it

```bash
make setup   # create a virtualenv
make run     # runs the sample workload with logging on
make test    # runs the sanity test
```

## Code walkthrough

- [`src/observe.py`](src/observe.py) — configures `logging`, defines a `timed`
  context manager, and runs a small workload that logs at `INFO` and `DEBUG`.
  Notice logs go to **stderr** with timestamps and levels — not bare prints.
- [`tests/test_observe.py`](tests/test_observe.py) — asserts the workload returns
  the expected result and that `timed` yields a positive duration.

## Try it yourself

- Add a `WARNING` log when the workload takes longer than a threshold.
- Switch the log format to JSON for machine parsing.

## Links

- 📺 Video: _TODO_
- 📄 Prev: [003 — Dev Tooling: Editor Setup](../003-dev-tooling-editor-setup/)
- 📄 Next: [005 — Build Your Own CLI (Python)](../005-build-your-own-cli-python/)
