from app.workers.jobs.transcript import process_transcript
from app.workers.queue import redis_settings


class WorkerSettings:
    """Arq worker entrypoint: `arq app.workers.worker.WorkerSettings`."""

    functions = [process_transcript]
    redis_settings = redis_settings()
    max_tries = 3
