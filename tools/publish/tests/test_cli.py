"""End-to-end CLI tests via Typer's runner."""

from typer.testing import CliRunner

from publish.cli import app

runner = CliRunner()


def test_new_command(repo):
    result = runner.invoke(app, ["new", "file-watcher", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    assert "created episodes/001-file-watcher" in result.output
    assert (repo / "episodes" / "001-file-watcher" / "README.md").is_file()


def test_check_command_passes(make_episode, repo):
    make_episode("001-demo", makefile="ok")
    result = runner.invoke(app, ["check", "001", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    assert "all checks passed" in result.output


def test_check_command_fails_on_todo(make_episode, repo):
    make_episode("001-demo", todos=True, makefile="ok")
    result = runner.invoke(app, ["check", "001", "--no-run", "--repo", str(repo)])
    assert result.exit_code == 1
    assert "FAIL" in result.output


def test_shorts_command(make_episode, repo):
    episode = make_episode("001-demo")
    (episode / "script.md").write_text(
        "[SHORT: One]\nhello world\n[/SHORT]\n", encoding="utf-8"
    )
    result = runner.invoke(app, ["shorts", "001", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    assert (episode / "shorts" / "short-01-one.md").is_file()
    assert "expected 3" in result.output  # only one block here


def test_shorts_command_no_script(make_episode, repo):
    make_episode("001-demo")
    result = runner.invoke(app, ["shorts", "001", "--repo", str(repo)])
    assert result.exit_code != 0
    assert "No episode script" in result.output


def test_release_dry_run(make_episode, repo):
    make_episode("002-demo")
    result = runner.invoke(app, ["release", "002", "--dry-run", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    assert "ep-002" in result.output
    assert "Manual YouTube Studio steps" in result.output
    assert "dry run" in result.output


def test_unknown_episode_exits_2(repo):
    result = runner.invoke(app, ["check", "999", "--repo", str(repo)])
    assert result.exit_code == 2
    assert "error:" in result.output
