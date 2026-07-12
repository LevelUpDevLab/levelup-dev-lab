# 001 — Automation: Hello, World

> Pillar: _Automation Recipes_ · Language(s): _Python_

## Summary

Your very first automation: a tiny Python script that greets you and prints the
current time. It's the "hello world" of the channel — proof your toolchain runs
end to end before we build anything real.

## What you'll learn

- How every episode is laid out (`src/`, `tests/`, `Makefile`).
- Running a Python script and its tests with `make`.
- Writing a function that's easy to test (return a value, don't just print).

## Prereqs

- Python 3.9+
- `make`

## Run it

```bash
make setup   # create a virtualenv (no third-party deps needed)
make run     # prints the greeting
make test    # runs the sanity test
```

## Code walkthrough

- [`src/hello.py`](src/hello.py) — `greet(name)` **returns** a string instead of
  printing it. That one habit makes the logic testable. `main()` handles the
  printing, and the `if __name__ == "__main__"` guard lets the file be both a
  script and an importable module.
- [`tests/test_hello.py`](tests/test_hello.py) — a single assertion that
  `greet("World")` contains what we expect.

## Try it yourself

- Make `greet` read the name from a command-line argument.
- Add a `--shout` flag that upper-cases the greeting.

## Links

- 📺 Video: _TODO_
- 📄 Next: [002 — Clean Code: Naming](../002-clean-code-naming/)
