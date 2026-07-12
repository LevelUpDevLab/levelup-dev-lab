# 001 — Automation: Hello, World

> Pillar: _Automation Recipes_ · Language(s): _Python_

## Summary

A realistic first automation: point it at a messy folder and it writes a single
Markdown status report — `report.md` — that groups the files by extension and
lists each file's size and last-modified date. It's the kind of chore you'd
otherwise do by hand, built with nothing but the Python standard library.

## What you'll learn

- Structuring a small tool as a package you can run with `python -m`.
- Using `argparse` for a real `--help`, flags, and exit codes — no CLI library.
- `pathlib` + `os.stat` to read file metadata, and `logging` (not `print`) for output.
- Writing testable code: pure functions, an injectable clock, and a pytest suite
  that covers the happy path and the error paths.

## Prereqs

- Python 3.11+
- `make`
- Standard library only — nothing to `pip install` to run it.

## Run it

```bash
make setup   # create a virtualenv and install pytest (for the tests only)
make run     # scans this episode folder and writes ./report.md
make test    # runs the pytest suite

# Run it against any folder yourself:
python -m automation_hello_world ~/Downloads
python -m automation_hello_world ~/Downloads -o downloads.md -v
python -m automation_hello_world --help
```

The tool exits `0` on success and non-zero on failure (e.g. `2` when the folder
doesn't exist), so it behaves in a shell script or CI step.

## Code walkthrough

The package is split so each piece does one job:

- [`automation_hello_world/scanner.py`](automation_hello_world/scanner.py) —
  `scan_folder()` walks the folder's top-level files and returns a list of
  `FileEntry` records (name, extension, size, modified time).
- [`automation_hello_world/report.py`](automation_hello_world/report.py) —
  `build_report()` groups those records by extension and renders the Markdown;
  `human_size()` formats byte counts.
- [`automation_hello_world/cli.py`](automation_hello_world/cli.py) —
  `argparse` wiring, logging config, and `main()` which glues scan → build →
  write together and returns the exit code.
- [`automation_hello_world/__main__.py`](automation_hello_world/__main__.py) —
  the one line that makes `python -m automation_hello_world` work.

For a paragraph-by-paragraph tour of each function (the way it's explained in the
video), see [`walkthrough.md`](walkthrough.md).

## Try it yourself

- Make the scan **recursive** so it descends into subfolders (hint: `Path.rglob`).
- Add a `--sort-by size` option to order files by size instead of name.
- Add a "largest files" section that lists the top 5 files overall.

## Links

- 📺 Video: _TODO_
- 📄 Next: [002 — Clean Code: Naming](../002-clean-code-naming/)
- 📚 Docs: [`argparse`](https://docs.python.org/3/library/argparse.html) ·
  [`pathlib`](https://docs.python.org/3/library/pathlib.html) ·
  [`logging`](https://docs.python.org/3/library/logging.html)
