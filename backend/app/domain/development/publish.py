"""Publishing generated code as a pull request (Story 6.4, FR-15). A branch + PR are created;
nothing is ever auto-merged or auto-deployed (NFR: human review gate, Idea.MD §27, §32).

MockGitPublisher runs offline for dev/tests; GitHubPublisher is gated behind GIT_PUBLISHER=github
and needs GITHUB_TOKEN + a target repo. The real path is not exercised offline."""

from typing import Protocol

from app.ai.schemas.development import PullRequest
from app.core.config import settings


class GitPublisher(Protocol):
    name: str

    async def publish(
        self, *, workspace: str, branch: str, title: str, body: str
    ) -> PullRequest: ...


class MockGitPublisher:
    """Deterministic publisher for offline dev/tests. Reports a branch + placeholder PR URL
    without touching a real remote."""

    name = "mock"

    async def publish(self, *, workspace: str, branch: str, title: str, body: str) -> PullRequest:
        repo = settings.github_repo or "protoflow/generated"
        return PullRequest(branch=branch, url=f"https://example.invalid/{repo}/pull/1", number=1)


class GitHubPublisher:
    """Pushes the workspace branch and opens a PR via the GitHub API. Gated and lazy so the mock
    path needs no token. Never merges."""

    name = "github"

    async def publish(self, *, workspace: str, branch: str, title: str, body: str) -> PullRequest:
        if not settings.github_token or not settings.github_repo:
            raise RuntimeError(
                "GitHubPublisher needs GITHUB_TOKEN and GITHUB_REPO (owner/repo) to be set."
            )
        import httpx  # local import: only needed on the real path

        owner_repo = settings.github_repo
        headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
        }
        # NOTE: assumes the branch has already been pushed to the remote (git plumbing lives in
        # Story 6.5's isolated executor). Here we only open the PR — never merge.
        async with httpx.AsyncClient(timeout=30) as client:  # pragma: no cover - live only
            resp = await client.post(
                f"https://api.github.com/repos/{owner_repo}/pulls",
                headers=headers,
                json={"title": title, "body": body, "head": branch, "base": "main"},
            )
            resp.raise_for_status()
            data = resp.json()
        return PullRequest(branch=branch, url=data["html_url"], number=data.get("number"))


def get_git_publisher() -> GitPublisher:
    """Return the configured git publisher (GIT_PUBLISHER: mock | github)."""
    if settings.git_publisher == "github":
        return GitHubPublisher()
    return MockGitPublisher()
