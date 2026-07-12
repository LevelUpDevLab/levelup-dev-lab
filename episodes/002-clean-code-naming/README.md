# 002 — Clean Code: Naming

> Pillar: _Best Practices_ · Language(s): _Python, Java, JavaScript_

## Summary

The same tiny function in three languages, refactored from cryptic names to
intention-revealing ones. Good names are the cheapest documentation you'll ever
write — this episode shows what "good" looks like across Python, Java, and JS.

## What you'll learn

- Why `d`, `tmp`, and `data` cost you later.
- Naming conventions per language: `snake_case` (Python), `camelCase`/`PascalCase`
  (Java, JS).
- How the _same idea_ reads in three ecosystems.

## Prereqs

- Python 3.9+
- Node 18+
- JDK 17+ (only needed for the Java example)
- `make`

## Run it

```bash
make setup       # sets up the Python venv (Java/JS need no install here)
make run         # runs all three examples
make run-python  # or run just one language
make run-node
make run-java
make test        # runs the sanity tests
```

## Code walkthrough

Each file computes the number of days a library book is overdue — the point is
the **names**, not the math.

- [`src/python/overdue.py`](src/python/overdue.py) — `days_overdue(due_date, returned_date)`.
- [`src/javascript/overdue.js`](src/javascript/overdue.js) — `daysOverdue(dueDate, returnedDate)`.
- [`src/java/Overdue.java`](src/java/Overdue.java) — `Overdue.daysOverdue(dueDate, returnedDate)`.

Compare them: different syntax, identical intent, and you can read every one
without a comment.

## Try it yourself

- Add a `lateFee(daysOverdue)` function with a clear, unit-bearing name.
- Rename a badly-named variable in your own project and notice the diff.

## Links

- 📺 Video: _TODO_
- 📄 Prev: [001 — Automation: Hello, World](../001-automation-hello-world/)
- 📄 Next: [003 — Dev Tooling: Editor Setup](../003-dev-tooling-editor-setup/)
