"""Typer CLI for the LevelUp Dev Lab per-episode publishing workflow."""

from pathlib import Path
from typing import Optional

import typer

from . import check as check_mod
from . import release as release_mod
from . import scaffold as scaffold_mod
from . import shorts as shorts_mod
from .config import PublishError, resolve_episode, resolve_repo_root

app = typer.Typer(
    help="Automate the per-episode publishing workflow for LevelUp Dev Lab.",
    no_args_is_help=True,
    add_completion=False,
)


def _fail(message: str, code: int = 2) -> "typer.Exit":
    typer.secho(f"error: {message}", fg=typer.colors.RED, err=True)
    return typer.Exit(code)


def _repo(repo: Optional[Path]) -> Path:
    try:
        return resolve_repo_root(repo)
    except PublishError as exc:
        raise _fail(str(exc))


def _episode(repo_root: Path, slug: str) -> Path:
    try:
        return resolve_episode(repo_root, slug)
    except PublishError as exc:
        raise _fail(str(exc))


@app.command()
def new(
    slug: str = typer.Argument(..., help="Episode slug, e.g. automation-file-watcher"),
    number: Optional[int] = typer.Option(
        None, "--number", "-n", help="Force an episode number instead of autonumbering."
    ),
    repo: Optional[Path] = typer.Option(
        None, "--repo", help="Path to the repo root (default: autodetect)."
    ),
) -> None:
    """Scaffold a new episode folder from the shared template."""
    repo_root = _repo(repo)
    try:
        episode = scaffold_mod.scaffold_episode(repo_root, slug, number)
    except PublishError as exc:
        raise _fail(str(exc))
    typer.secho(f"created {episode.relative_to(repo_root)}", fg=typer.colors.GREEN)
    typer.echo("next: fill in README.md + walkthrough.md, then run `publish check`.")


@app.command()
def check(
    slug: str = typer.Argument(..., help="Episode slug, number, or folder name."),
    run: bool = typer.Option(True, help="Run `make run` and `make test`."),
    setup: bool = typer.Option(True, help="Run `make setup` before run/test."),
    repo: Optional[Path] = typer.Option(
        None, "--repo", help="Path to the repo root (default: autodetect)."
    ),
) -> None:
    """Validate an episode: README sections, walkthrough, no TODOs, code runs, tests pass."""
    repo_root = _repo(repo)
    episode = _episode(repo_root, slug)
    try:
        results = check_mod.check_episode(episode, run_code=run, setup=setup)
    except PublishError as exc:
        raise _fail(str(exc))

    failures = 0
    for result in results:
        mark = "PASS" if result.ok else "FAIL"
        color = typer.colors.GREEN if result.ok else typer.colors.RED
        line = f"[{mark}] {result.name}"
        if result.detail:
            line += f" — {result.detail}"
        typer.secho(line, fg=color)
        failures += 0 if result.ok else 1

    if failures:
        typer.secho(f"\n{failures} check(s) failed", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    typer.secho("\nall checks passed", fg=typer.colors.GREEN)


@app.command()
def shorts(
    slug: str = typer.Argument(..., help="Episode slug, number, or folder name."),
    repo: Optional[Path] = typer.Option(
        None, "--repo", help="Path to the repo root (default: autodetect)."
    ),
) -> None:
    """Extract [SHORT] segments from the episode script into shorts/*.md."""
    repo_root = _repo(repo)
    episode = _episode(repo_root, slug)
    try:
        script = shorts_mod.find_script(episode)
    except PublishError as exc:
        raise _fail(str(exc))

    segments = shorts_mod.extract_shorts(script.read_text(encoding="utf-8"))
    if not segments:
        raise _fail("no [SHORT] blocks found in the script", code=1)

    written = shorts_mod.write_shorts(episode, segments)
    for segment, path in zip(segments, written):
        flag = "ok" if segment.in_range else "OUT OF RANGE"
        typer.echo(
            f"  {path.relative_to(repo_root)}  ({segment.est_seconds:.0f}s, {flag})"
        )
    if len(segments) != 3:
        typer.secho(
            f"note: found {len(segments)} [SHORT] block(s), expected 3",
            fg=typer.colors.YELLOW,
        )
    typer.secho(f"wrote {len(written)} short(s)", fg=typer.colors.GREEN)


@app.command()
def release(
    slug: str = typer.Argument(..., help="Episode slug, number, or folder name."),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print notes + checklist without creating the tag."
    ),
    notes_file: bool = typer.Option(
        True, help="Also write RELEASE_NOTES.md into the episode folder."
    ),
    repo: Optional[Path] = typer.Option(
        None, "--repo", help="Path to the repo root (default: autodetect)."
    ),
) -> None:
    """Tag the episode, generate release notes from its README, print the YouTube checklist."""
    repo_root = _repo(repo)
    episode = _episode(repo_root, slug)
    try:
        info = release_mod.build_release(episode)
    except PublishError as exc:
        raise _fail(str(exc))

    if notes_file:
        (episode / "RELEASE_NOTES.md").write_text(info.notes, encoding="utf-8")

    typer.secho(f"== release notes ({info.tag}) ==", fg=typer.colors.CYAN)
    typer.echo(info.notes)

    if dry_run:
        typer.secho(f"dry run: would create tag {info.tag}", fg=typer.colors.YELLOW)
    else:
        try:
            release_mod.create_tag(repo_root, info.tag, info.notes)
        except PublishError as exc:
            raise _fail(str(exc))
        typer.secho(
            f"created tag {info.tag} (push with: git push origin {info.tag})",
            fg=typer.colors.GREEN,
        )

    typer.echo("")
    typer.echo(release_mod.render_checklist(info, episode.name))


def main() -> None:
    """Console-script entry point."""
    app()
