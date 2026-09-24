import enum

from pydantic import BaseModel, Field


class TestStatus(enum.StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class TestCase(BaseModel):
    """A test generated from the MVP's requirements/acceptance criteria (FR-16). `feature` links
    it back to the MVP feature it validates, for end-to-end traceability (FR-17)."""

    id: str
    feature: str = ""
    title: str
    steps: list[str] = Field(default_factory=list)
    expected: str = ""
    status: TestStatus = TestStatus.PASS
    evidence: str = ""
    failure_reason: str | None = None


class TestCaseList(BaseModel):
    test_cases: list[TestCase] = Field(default_factory=list)


class FeatureCoverage(BaseModel):
    feature: str
    scope: str
    covered: bool
    test_ids: list[str] = Field(default_factory=list)


class QAReport(BaseModel):
    """Coverage rollup and pass/fail counts for the implemented MVP (FR-17)."""

    test_cases: list[TestCase] = Field(default_factory=list)
    coverage: list[FeatureCoverage] = Field(default_factory=list)
    total: int = 0
    passed: int = 0
    failed: int = 0
    blocked: int = 0
    must_have_covered: bool = False
    demo_ready: bool = False
