# 003 — Dev Tooling: Editor Setup

> Pillar: _Dev Tooling_ · Language(s): _Language-agnostic_

## Summary

A portable editor baseline that follows you across projects: an `.editorconfig`
plus a starter VS Code `settings.json`. No language runtime required — this
episode is about the tools around your code.

## What you'll learn

- What `.editorconfig` does and why every repo should have one.
- A sane set of editor defaults (format on save, trim whitespace, final newline).
- How to verify your config is present with a quick sanity check.

## Prereqs

- `bash` and `make` (that's it — this episode is language-agnostic).
- A text editor that reads EditorConfig (most do, natively or via a plugin).

## Run it

```bash
make setup   # nothing to install — prints a checklist
make run     # prints the sample config and how to apply it
make test    # verifies the sample config files are present and non-empty
```

## Code walkthrough

- [`src/.editorconfig`](src/.editorconfig) — a minimal, copy-me-into-any-repo baseline.
- [`src/vscode-settings.json`](src/vscode-settings.json) — editor defaults that
  pair well with EditorConfig (format on save, rulers, trim on save).
- [`src/check_setup.sh`](src/check_setup.sh) — the sanity check `make test` runs.

## Try it yourself

- Copy `src/.editorconfig` into one of your own repos and commit it.
- Add a rule for a file type you use that isn't covered yet.

## Links

- 📺 Video: _TODO_
- 📄 Prev: [002 — Clean Code: Naming](../002-clean-code-naming/)
- 📄 Next: [004 — Observability Basics](../004-observability-basics/)
