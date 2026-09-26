import sys

from app.domain.development.sandbox import SubprocessSandbox, get_sandbox


def test_subprocess_sandbox_is_default():
    assert get_sandbox().name == "subprocess"


async def test_sandbox_runs_in_workspace_cwd(tmp_path):
    result = await SubprocessSandbox().run(
        workspace=str(tmp_path),
        command=[sys.executable, "-c", "import os; print(os.getcwd())"],
    )
    assert result.exit_code == 0
    assert str(tmp_path) in result.stdout


async def test_sandbox_scrubs_app_secrets(tmp_path, monkeypatch):
    # A secret in the app process must NOT be visible to sandboxed code (NFR5).
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-not-leak")
    result = await SubprocessSandbox().run(
        workspace=str(tmp_path),
        command=[sys.executable, "-c", "import os; print(os.environ.get('ANTHROPIC_API_KEY'))"],
    )
    assert result.exit_code == 0
    assert "sk-should-not-leak" not in result.stdout
    assert "None" in result.stdout


async def test_sandbox_enforces_timeout(tmp_path):
    result = await SubprocessSandbox().run(
        workspace=str(tmp_path),
        command=[sys.executable, "-c", "import time; time.sleep(5)"],
        timeout=1,
    )
    assert result.timed_out is True
    assert result.exit_code == -1


async def test_sandbox_captures_nonzero_exit(tmp_path):
    result = await SubprocessSandbox().run(
        workspace=str(tmp_path),
        command=[sys.executable, "-c", "import sys; sys.exit(3)"],
    )
    assert result.exit_code == 3
