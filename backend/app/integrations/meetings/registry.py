from app.integrations.meetings.base import MeetingProvider
from app.integrations.meetings.mock import MockMeetingProvider

_PROVIDERS: dict[str, MeetingProvider] = {
    "mock": MockMeetingProvider(),
}


def get_provider(name: str) -> MeetingProvider:
    if name not in _PROVIDERS:
        raise KeyError(f"Unknown meeting provider: {name}")
    return _PROVIDERS[name]
