import pytest

from app.domain.development.publish import (
    GitHubPublisher,
    MockGitPublisher,
    get_git_publisher,
)


def test_mock_publisher_is_default():
    assert get_git_publisher().name == "mock"


async def test_mock_publisher_returns_branch_and_pr_url():
    pr = await MockGitPublisher().publish(
        workspace="/tmp/x", branch="protoflow/generated-mvp", title="t", body="b"
    )
    assert pr.branch == "protoflow/generated-mvp"
    assert pr.url.startswith("https://")
    assert pr.number == 1


async def test_github_publisher_requires_credentials(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "github_token", None)
    monkeypatch.setattr(settings, "github_repo", None)
    with pytest.raises(RuntimeError):
        await GitHubPublisher().publish(workspace="/tmp/x", branch="b", title="t", body="b")
