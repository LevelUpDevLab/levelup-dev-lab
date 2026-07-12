# Walkthrough — Episode 001

This is the narration track: one short paragraph per function, in the order I'd
talk through them on camera. Skim the code alongside it.

## `scanner.py`

**`AutomationError`** — This is just a small custom exception. Whenever something
goes wrong that's really the _user's_ fault rather than a bug — a folder that
doesn't exist, a path that turns out to be a file — I raise this. Having a
dedicated type means the CLI layer can catch exactly these, print a clean
message, and exit non-zero, without accidentally swallowing real programming
errors.

**`FileEntry`** — A frozen dataclass holding the four things the report actually
uses: the file's name, its extension, its size in bytes, and when it was last
modified. I like pulling this out into its own type early. The rest of the code
gets to pass around one tidy object instead of loose tuples, and `frozen=True`
means once I've recorded a file, nothing downstream can quietly mutate it.

**`scan_folder`** — This is the part that touches the disk. It checks the path
exists and is a folder up front — failing fast with a clear message beats a
confusing crash three functions later. Then it iterates the folder's top-level
entries, skips anything that isn't a file, calls `stat()` once per file to get
size and modified time, and builds a `FileEntry` for each. It deliberately does
_not_ recurse into subfolders — keeping it flat keeps the episode focused, and
recursion is a nice exercise to add yourself.

## `report.py`

**`human_size`** — A tiny formatter that turns a raw byte count into something a
human wants to read, like `1.5 KB` instead of `1536`. It walks up the units
until the number fits under 1024, showing whole bytes but one decimal place for
everything larger. Nothing clever — but it's the difference between a report you
skim and one you squint at.

**`build_report`** — The heart of the episode. It takes the list of files and
returns the whole Markdown document as a string — note it returns text rather
than writing a file, which is what makes it easy to test. It handles the empty
folder case first, then computes the totals, groups the files by extension once,
and renders two tables: a summary of counts and sizes per extension, and a
detailed per-extension listing. The `now` argument looks odd until you see the
tests — injecting the clock lets me pin the "Generated" timestamp so the output
is deterministic.

## `cli.py`

**`build_parser`** — All the `argparse` setup lives here, on its own, so a test
can build the parser without running anything. It defines the one positional
argument (the folder), the `--output` path that defaults to `report.md`, a
`-v` flag for more logging, and `--version`. The `description` and `epilog` are
what show up in `--help`, so I write them as if that's the only docs someone
reads — because often it is.

**`configure_logging`** — One small function that decides how chatty the tool is.
By default you get `INFO` — enough to confirm what it did — and passing `-v`
switches on `DEBUG` so you can watch it skip directories and see the group count.
Everything goes through `logging` to stderr, never `print`, so the real output
(the report file) and the diagnostics stay cleanly separated.

**`main`** — The glue. It parses the arguments, sets up logging, then runs the
three steps in order: scan the folder, build the report, write it out. Each risky
step is wrapped so a bad folder or an unwritable path becomes a logged error and
a return code of `2`, not a stack trace. It returns an integer exit code instead
of calling `exit()` itself — that keeps `main` testable, and `__main__.py` is the
one place that actually hands the code back to the shell.

## `__main__.py`

**`__main__` module** — This is the two-line file that makes
`python -m automation_hello_world` work. It imports `main`, and when the module
is run directly it calls it and hands the return value to `SystemExit`, which is
what sets the process exit code. Small, but it's the seam between "importable
library" and "runnable command."
