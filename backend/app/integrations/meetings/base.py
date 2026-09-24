from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class SegmentData:
    speaker: str
    start_time: int
    end_time: int
    text: str


@dataclass
class MeetingData:
    external_meeting_id: str
    title: str
    participants: list[str] = field(default_factory=list)


@dataclass
class TranscriptData:
    external_meeting_id: str
    language: str
    segments: list[SegmentData] = field(default_factory=list)


@runtime_checkable
class MeetingProvider(Protocol):
    """Decouples business logic from any specific meeting platform (Idea.MD §48)."""

    name: str

    async def get_meeting(self, external_meeting_id: str) -> MeetingData: ...

    async def get_transcript(self, external_meeting_id: str) -> TranscriptData: ...

    async def verify_webhook(self, headers: dict[str, str], body: bytes) -> bool: ...
