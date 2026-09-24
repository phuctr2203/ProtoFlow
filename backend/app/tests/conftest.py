from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.db.models  # noqa: F401  (register models on Base.metadata)
from app.core.config import settings
from app.db.base import Base
from app.db.database import get_session
from app.main import app
from app.workers.queue import get_queue


@pytest.fixture(autouse=True)
def _force_mock_llm():
    """Tests use the deterministic mock provider regardless of the ambient
    LLM_PROVIDER env, so the suite never makes real API calls."""
    original = settings.llm_provider
    settings.llm_provider = "mock"
    yield
    settings.llm_provider = original


class FakeQueue:
    """Records enqueue_job calls instead of talking to Redis."""

    def __init__(self) -> None:
        self.jobs: list[tuple[str, tuple]] = []

    async def enqueue_job(self, function: str, *args: object) -> None:
        self.jobs.append((function, args))
        return None


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
def fake_queue():
    return FakeQueue()


@pytest_asyncio.fixture
async def client(session_factory, fake_queue) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session() -> AsyncGenerator:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_queue] = lambda: fake_queue

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
