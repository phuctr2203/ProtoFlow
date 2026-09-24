from app.workers.jobs.intelligence import process_meeting_intelligence
from app.workers.jobs.transcript import process_transcript
from app.workers.queue import redis_settings


class WorkerSettings:
    """Arq worker entrypoint: `arq app.workers.worker.WorkerSettings`."""

    functions = [process_transcript, process_meeting_intelligence]
    redis_settings = redis_settings()
    max_tries = 3
