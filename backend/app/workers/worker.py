from app.workers.jobs.code_generation import process_code_generation
from app.workers.jobs.design import process_design
from app.workers.jobs.intelligence import process_meeting_intelligence
from app.workers.jobs.mvp import process_mvp
from app.workers.jobs.transcript import process_transcript
from app.workers.queue import redis_settings


class WorkerSettings:
    """Arq worker entrypoint: `arq app.workers.worker.WorkerSettings`."""

    functions = [
        process_transcript,
        process_meeting_intelligence,
        process_mvp,
        process_design,
        process_code_generation,
    ]
    redis_settings = redis_settings()
    max_tries = 3
