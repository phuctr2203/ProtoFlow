from app.integrations.meetings.base import MeetingData, TranscriptData
from app.integrations.meetings.fixtures import get_fixture


class MockMeetingProvider:
    """v1 meeting provider — serves pre-built transcript fixtures (Idea.MD §5.1).

    Real integration (e.g. self-hosted Jitsi) is a later, isolated swap-in behind
    the same MeetingProvider protocol.
    """

    name = "mock"

    async def get_meeting(self, external_meeting_id: str) -> MeetingData:
        meeting, _ = get_fixture(external_meeting_id)
        return meeting

    async def get_transcript(self, external_meeting_id: str) -> TranscriptData:
        _, transcript = get_fixture(external_meeting_id)
        return transcript

    async def verify_webhook(self, headers: dict[str, str], body: bytes) -> bool:
        # The mock provider accepts any locally-generated event. A real provider
        # verifies a signature here.
        return True
