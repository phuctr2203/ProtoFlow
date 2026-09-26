"""Isolated execution of generated code (Story 6.5, NFR5, Idea.MD §72). Generated code must never
run in the app process or see the app's secrets.

SubprocessSandbox (default) runs each command in a separate process, confined to the workspace cwd,
with a scrubbed environment (no ANTHROPIC/OLLAMA/DB/etc. secrets) and a hard timeout. DockerSandbox
(gated by SANDBOX_MODE=docker) runs the command in a throwaway, network-less container for stronger
isolation; it is not exercised offline."""

import asyncio
import os

from pydantic import BaseModel

from app.core.config import settings

# Only these environment keys are passed through to sandboxed code; everything else (all secrets)
# is withheld.
_ALLOWED_ENV = {"PATH", "LANG", "LC_ALL"}


class SandboxResult(BaseModel):
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False


def _scrubbed_env(workspace: str) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k in _ALLOWED_ENV}
    env["HOME"] = workspace
    return env


class SubprocessSandbox:
    name = "subprocess"

    async def run(
        self, *, workspace: str, command: list[str], timeout: int | None = None
    ) -> SandboxResult:
        limit = timeout or settings.sandbox_timeout_seconds
        proc = await asyncio.create_subprocess_exec(
            *command,
            cwd=workspace,
            env=_scrubbed_env(workspace),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=limit)
        except TimeoutError:
            proc.kill()
            await proc.communicate()
            return SandboxResult(exit_code=-1, timed_out=True)
        return SandboxResult(
            exit_code=proc.returncode if proc.returncode is not None else -1,
            stdout=out.decode(errors="replace"),
            stderr=err.decode(errors="replace"),
        )


class DockerSandbox:
    """Runs the command in a throwaway, network-less container with the workspace mounted. Gated;
    requires a Docker socket. Not exercised offline."""

    name = "docker"

    async def run(
        self, *, workspace: str, command: list[str], timeout: int | None = None
    ) -> SandboxResult:
        limit = timeout or settings.sandbox_timeout_seconds
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "-v",
            f"{workspace}:/ws",
            "-w",
            "/ws",
            settings.sandbox_image,
            *command,
        ]
        proc = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:  # pragma: no cover - requires a Docker socket
            out, err = await asyncio.wait_for(proc.communicate(), timeout=limit)
        except TimeoutError:  # pragma: no cover
            proc.kill()
            await proc.communicate()
            return SandboxResult(exit_code=-1, timed_out=True)
        return SandboxResult(  # pragma: no cover
            exit_code=proc.returncode if proc.returncode is not None else -1,
            stdout=out.decode(errors="replace"),
            stderr=err.decode(errors="replace"),
        )


def get_sandbox():
    """Return the configured sandbox (SANDBOX_MODE: subprocess | docker)."""
    if settings.sandbox_mode == "docker":
        return DockerSandbox()
    return SubprocessSandbox()
