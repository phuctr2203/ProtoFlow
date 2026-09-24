from collections.abc import AsyncGenerator

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings


def redis_settings() -> RedisSettings:
    return RedisSettings.from_dsn(settings.redis_url)


async def get_queue() -> AsyncGenerator:
    """FastAPI dependency yielding an Arq pool used to enqueue background jobs.

    Overridden in tests with a fake that records enqueues.
    """
    pool = await create_pool(redis_settings())
    try:
        yield pool
    finally:
        await pool.aclose()
