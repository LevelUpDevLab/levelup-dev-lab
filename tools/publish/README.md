# publish — LevelUp Dev Lab episode workflow

An internal Typer CLI that automates the per-episode publishing workflow. It is
also a worked example of the channel's "build your own tooling" pillar, so the
code is meant to be read.

## Install

```bash
make setup          # venv + editable install (pulls in Typer)
.venv/bin/publish --help
```

Or run without installing the console script:

```bash
python -m publish --help
```

## Commands

| Command                  | What it does                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `publish new <slug>`     | Scaffold `episodes/NNN-<slug>/` from the shared template (autonumbers).                                                        |
| `publish check <slug>`   | Validate an episode: README sections, `walkthrough.md`, no leftover TODOs, `make run` and `make test` pass.                    |
| `publish shorts <slug>`  | Extract `[SHORT]…[/SHORT]` blocks from the episode script into `shorts/*.md`, with a 60–90s duration estimate.                 |
| `publish release <slug>` | Create an annotated git tag (`ep-NNN`), generate release notes from the README, and print the manual YouTube Studio checklist. |

`<slug>` accepts the full folder name (`001-automation-hello-world`), the number
(`001` or `1`), or the descriptive part (`automation-hello-world`).

### Episode scripts and Shorts

`publish shorts` reads `episodes/<slug>/script.md` and looks for marked blocks:

```markdown
[SHORT: Why naming matters]
Here's the 60-second version. A good name is the cheapest documentation
you will ever write...
[/SHORT]
```

The title after the colon is optional. Each block is written to
`shorts/short-NN-title.md` with an estimated spoken duration flagged if it falls
outside the 60–90 second window.

## Layout

```
publish/
  config.py     paths, slug/episode resolution
  scaffold.py   `new`
  check.py      `check`
  shorts.py     `shorts`
  release.py    `release`
  cli.py        Typer wiring (thin; logic lives in the modules above)
tests/          pytest suite
```

The command modules are pure functions over paths and text; `cli.py` is a thin
Typer layer. That split is what makes the whole thing testable.

## Test

```bash
make test
```
