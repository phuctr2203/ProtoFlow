import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.db.models.meeting import MeetingStatus


class MeetingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    provider: str
    external_meeting_id: str
    title: str
    status: MeetingStatus
    created_at: datetime
    updated_at: datetime


class TranscriptSegmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    speaker: str
    start_time: int
    end_time: int
    text: str


class TranscriptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    language: str | None
    status: str
    segments: list[TranscriptSegmentRead]


class SimulateMeetingRequest(BaseModel):
    project_id: uuid.UUID
    fixture: str = "clean"
    title: str | None = None
