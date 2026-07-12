# 006 — Build Your Own CLI (Node)

> Pillar: _Build Your Own Tooling_ · Language(s): _JavaScript (Node)_

## Summary

The Node counterpart to episode 005: the same `wordcount` idea, built with Node's
`process.argv` and stdin. No dependencies — just the standard library — so you see
exactly how a CLI works under the hood.

## What you'll learn

- Parsing arguments from `process.argv` (and when to reach for a library instead).
- Reading from a file **or** stdin so the tool works in a pipe.
- Exporting a pure `count()` function so it's unit-testable.

## Prereqs

- Node 18+
- `make`

## Run it

```bash
make setup                       # installs dev deps (none required; runs npm if present)
make run                         # runs the CLI against sample input
echo "hello there" | node src/cli.js
node src/cli.js README.md --words
make test                        # runs the sanity test
```

## Code walkthrough

- [`src/cli.js`](src/cli.js) — `count(text)` returns `{ lines, words, chars }`
  (pure, testable). The bottom of the file reads a file arg or stdin, then prints
  the requested counts. Guarded by `require.main === module` so it can be imported.
- [`tests/cli.test.js`](tests/cli.test.js) — plain Node `assert`, no framework.

## Try it yourself

- Add a `--json` flag that prints the counts as JSON.
- Compare your `process.argv` parsing to a library like `yargs` or `commander`.

## Links

- 📺 Video: _TODO_
- 📄 Prev: [005 — Build Your Own CLI (Python)](../005-build-your-own-cli-python/)
- 📄 Back to [all episodes](../)
