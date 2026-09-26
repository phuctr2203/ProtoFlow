"""Authored 'expected' QA test cases for the document-Q&A MVP (Idea.MD §33). Used by the
MockLLMProvider so the QA pipeline runs offline. Each test maps to a MUST_HAVE MVP feature so
coverage resolves; statuses simulate an executed run."""

from app.ai.schemas.qa import TestCase, TestCaseList, TestStatus


def build_qa() -> TestCaseList:
    return TestCaseList(
        test_cases=[
            TestCase(
                id="TC-001",
                feature="Upload PDF documents",
                title="Upload a PDF and see it listed",
                steps=["POST /documents with a PDF", "GET /documents"],
                expected="The document appears in the list",
                status=TestStatus.PASS,
                evidence="Executed in sandbox; document listed.",
            ),
            TestCase(
                id="TC-002",
                feature="Process & chunk documents",
                title="Uploaded document is chunked and indexed",
                steps=["Upload a document", "Wait for ingestion"],
                expected="Chunks are embedded and stored",
                status=TestStatus.PASS,
                evidence="Executed in sandbox; chunks present.",
            ),
            TestCase(
                id="TC-003",
                feature="Ask natural-language questions",
                title="Ask a question about an uploaded document",
                steps=["POST /ask with a question"],
                expected="A relevant answer is returned",
                status=TestStatus.PASS,
                evidence="Executed in sandbox; answer returned.",
            ),
            TestCase(
                id="TC-004",
                feature="Retrieve relevant passages",
                title="Answer retrieves relevant passages",
                steps=["Ask a question", "Inspect retrieved chunks"],
                expected="Retrieved passages are relevant to the question",
                status=TestStatus.PASS,
                evidence="Executed in sandbox; relevant chunks retrieved.",
            ),
            TestCase(
                id="TC-005",
                feature="Generate answer with citations",
                title="Answer includes source citations",
                steps=["Ask a question", "Inspect the answer"],
                expected="The answer cites its sources",
                status=TestStatus.PASS,
                evidence="Executed in sandbox; citations present.",
            ),
        ]
    )
