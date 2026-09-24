"""Mock transcript fixtures — one shared 'document Q&A assistant' client scenario
(Idea.MD §71), each with a distinct noise profile so the downstream Evidence
Validator and confidence scoring are exercised beyond a clean happy path.
"""

from app.integrations.meetings.base import MeetingData, SegmentData, TranscriptData

# profile key -> (MeetingData, TranscriptData)
_FIXTURES: dict[str, tuple[MeetingData, TranscriptData]] = {
    "clean": (
        MeetingData("clean", "Acme discovery call", ["Consultant", "Client"]),
        TranscriptData(
            "clean",
            "en",
            [
                SegmentData("Client", 700, 712, "We have hundreds of internal documents."),
                SegmentData(
                    "Client", 713, 724, "Employees waste too much time searching for information."
                ),
                SegmentData("Client", 725, 730, "Most of our documents are PDF."),
                SegmentData(
                    "Client", 1102, 1115, "We want employees to ask questions in natural language."
                ),
                SegmentData(
                    "Consultant", 1116, 1122, "And the answer should show where it came from?"
                ),
                SegmentData("Client", 1123, 1130, "Yes, the answer should show its source."),
                SegmentData(
                    "Client", 1500, 1508, "For the first demo we only need a simple interface."
                ),
            ],
        ),
    ),
    "asr_noisy": (
        MeetingData("asr_noisy", "Acme discovery call (fast speech)", ["Consultant", "Client"]),
        TranscriptData(
            "asr_noisy",
            "en",
            [
                SegmentData(
                    "Client",
                    40,
                    52,
                    "we have hundreds of internal document employ waste to much time search for info",
                ),
                SegmentData("Client", 53, 60, "most of our document are pea dee eff"),
                SegmentData(
                    "Client", 320, 333, "we want employ to ask question in natural language"
                ),
                SegmentData("Client", 334, 341, "the anser should show were the info came from"),
                SegmentData("Consultant", 342, 349, "ok so citations to the sauce document"),
                SegmentData("Client", 900, 907, "for the fyrst demo just a simple interfase"),
            ],
        ),
    ),
    "diarization_noisy": (
        MeetingData(
            "diarization_noisy", "Acme discovery call (cross-talk)", ["Consultant", "Client"]
        ),
        TranscriptData(
            "diarization_noisy",
            "en",
            [
                SegmentData(
                    "Speaker 1",
                    10,
                    26,
                    "We have hundreds of internal documents employees waste time searching most are PDF",
                ),
                SegmentData(
                    "Unknown",
                    27,
                    40,
                    "we want employees to ask questions in natural language and the answer should show where it came from",
                ),
                SegmentData(
                    "Speaker 1", 300, 308, "for the first demo we only need a simple interface"
                ),
                SegmentData("Speaker 2", 309, 315, "understood, a simple interface first"),
            ],
        ),
    ),
    "mixed_language": (
        MeetingData("mixed_language", "Acme discovery call (VN/EN)", ["Consultant", "Client"]),
        TranscriptData(
            "mixed_language",
            "vi",
            [
                SegmentData("Client", 60, 74, "Chúng tôi có hàng trăm tài liệu nội bộ."),
                SegmentData(
                    "Client", 75, 88, "Nhân viên mất quá nhiều thời gian để tìm kiếm thông tin."
                ),
                SegmentData("Client", 89, 96, "Most documents are PDF, một số bằng tiếng Việt."),
                SegmentData(
                    "Client", 300, 312, "We want employees to ask questions bằng ngôn ngữ tự nhiên."
                ),
                SegmentData("Client", 313, 320, "The answer should show nguồn thông tin."),
            ],
        ),
    ),
    "combined": (
        MeetingData("combined", "Acme discovery call (noisy + VN/EN)", ["Consultant", "Client"]),
        TranscriptData(
            "combined",
            "vi",
            [
                SegmentData(
                    "Speaker 1",
                    12,
                    30,
                    "we have hundred of internal document nhan vien mat thoi gian tim kiem most are pea dee eff",
                ),
                SegmentData(
                    "Unknown",
                    31,
                    44,
                    "want employ to ask question natural language anser show were info came from mot so tieng viet",
                ),
                SegmentData("Speaker 1", 260, 268, "first demo just simple interfase"),
            ],
        ),
    ),
}

PROFILES = list(_FIXTURES.keys())


def get_fixture(external_meeting_id: str) -> tuple[MeetingData, TranscriptData]:
    if external_meeting_id not in _FIXTURES:
        raise KeyError(f"Unknown mock transcript fixture: {external_meeting_id}")
    return _FIXTURES[external_meeting_id]
