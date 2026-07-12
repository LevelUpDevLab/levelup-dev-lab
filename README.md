# LevelUp Dev Lab

> **Our promise:** Help entry-level devs think and build like engineers.

This is the companion repository for the **LevelUp Dev Lab** YouTube channel.
Every episode ships as a small, self-contained project you can clone, run, and
break on your own machine — in **Python**, **Java**, or **JavaScript**.

## Content pillars

Everything we make falls under one of four pillars:

1. **Automation Recipes** — small scripts that delete busywork.
2. **Best Practices** — the habits that separate juniors from engineers.
3. **Dev Tooling** — configure and master the tools you already use.
4. **Build Your Own Tooling** — go from _tool user_ to _tool maker_.

## Episodes

| #   | Episode                                                                | Language(s)              |
| --- | ---------------------------------------------------------------------- | ------------------------ |
| 001 | [Automation: Hello, World](episodes/001-automation-hello-world/)       | Python                   |
| 002 | [Clean Code: Naming](episodes/002-clean-code-naming/)                  | Python, Java, JavaScript |
| 003 | [Dev Tooling: Editor Setup](episodes/003-dev-tooling-editor-setup/)    | Language-agnostic        |
| 004 | [Observability Basics](episodes/004-observability-basics/)             | Python                   |
| 005 | [Build Your Own CLI (Python)](episodes/005-build-your-own-cli-python/) | Python                   |
| 006 | [Build Your Own CLI (Node)](episodes/006-build-your-own-cli-node/)     | JavaScript               |

New episodes land in [`episodes/`](episodes/). Shared templates and scaffolding
scripts live in [`shared/`](shared/).

## How to use this repo

Each episode is standalone. To work through one:

```bash
# 1. Clone the repo
git clone https://github.com/<your-user>/levelup-dev-lab.git
cd levelup-dev-lab

# 2. Change into the episode you're watching
cd episodes/001-automation-hello-world

# 3. Follow that episode's README
#    (every episode has its own README, Makefile, src/, and tests/)
cat README.md
make setup   # install anything the episode needs
make run     # run the example
make test    # run the sanity tests
```

Each episode's `README.md` is the source of truth for that episode — the
Makefile targets (`setup`, `run`, `test`) work the same way everywhere, but
they delegate to whatever toolchain that episode needs.

## CI

Every push and pull request runs [GitHub Actions](.github/workflows/ci.yml):
each episode's `make setup` + `make test` runs in its own matrix job (Python,
Node, and Java are all available), plus a `pre-commit` job that enforces
formatting and lint.

## Contributing

PRs and issues are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
