# PRD Addendum: ProtoFlow

Technical-how content and depth that doesn't belong in the PRD itself but should carry forward into downstream work (`bmad-architecture`, `bmad-create-epics-and-stories`).

## Technology Stack Decisions
- **Backend:** Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic, asyncpg, managed via `uv`.
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Query, managed via `npm`.
- **Database:** PostgreSQL (system of record).
- **Job queue:** Arq (async, Redis-backed) — chosen over Celery (too heavy for this scale) and RQ (sync-only, doesn't fit FastAPI's async style).
- **LLM access:** a custom `LLMProvider` abstraction layer, deliberately not relying directly on LangChain's chat-model interface, so the underlying provider or even framework can be swapped later with minimal ripple through the app. Built on top of LangGraph for agent orchestration.
- **Vector DB:** Qdrant — introduced only in the AI-Assisted Development feature (PRD §5.6) when the generated sample MVP first needs retrieval, not before.
- **Object storage:** MinIO (local) / Azure Blob (future) — introduced at the same point as Qdrant, for document/artifact storage.
- **Observability:** structured logs + LangSmith tracing (from the Meeting Intelligence feature onward).

## Docker Compose Service Introduction Timing
Rather than running the full service list from day one, services are added when a phase actually uses them:
- Foundation: `postgres`, `redis`, `backend`, `frontend`.
- Meeting Integration: + `worker` (Arq).
- AI-Assisted Development: + `qdrant`, `minio`.

## Meeting Provider Abstraction
A `MeetingProvider` protocol decouples business logic from any specific meeting platform (`get_meeting`, `get_transcript`, `verify_webhook`). v1 ships only a `MockMeetingProvider`. Real integration is deferred; when it happens, the user leans toward self-hosted Jitsi + Jigasi (open source, more infra work, full control) over JaaS/8x8 (paid, faster to integrate, vendor dependency) — not yet committed.

## Mock Transcript Fixture Design
~5 fixture transcripts, all built around the spec's own simple "document Q&A assistant" client scenario (avoid inventing a more complex scenario), each with a distinct noise profile so the Evidence Validator and confidence-scoring logic are genuinely exercised rather than only tested against a clean happy path:
1. **Clean** — correct speakers, complete sentences.
2. **ASR-noisy** — word-level errors simulating fast/unclear speech (homophones, garbled words, missing punctuation).
3. **Diarization-noisy** — wrong or missing speaker attribution, overlapping speakers merged into one segment.
4. **Mixed-language** — non-English or code-switched segments (the spec's own example already mentions Vietnamese documents).
5. **Combined** — at least two of the above noise types together.

These fixtures double as the evaluation dataset for meeting-intelligence accuracy (precision/recall/faithfulness/evidence accuracy).

## Competitive Landscape (research digest, 2026-09-17)
- Meeting-intelligence tools (Fathom, Fireflies, Otter, Gong/Chorus) stop at summaries/action items — built for CRM/sales workflows, not engineering handoff.
- "Requirements AI" and similar tools convert transcripts to structured requirements but stop there — no MVP scoping or code generation follows.
- Prompt-to-app generators (v0, Bolt, Lovable, Replit Agent, Claude Code/Cursor as the underlying agentic layer) start from a human-written prompt, not a raw meeting.
- No product found chains meeting → traceable requirements → MVP scoping → approval gate → design → code → QA → honest demo as one connected flow — this is ProtoFlow's differentiation.
- Risks informing PRD §9 Constraints: hallucinated requirements/code, dependency/package hallucination, client trust collapse from a single visible demo error, developers shipping AI code they don't fully understand, scope creep without traceability.

## Existing Phase-by-Phase Plan
`docs/plan.md` (in the repo) already captures a hand-written phase-by-phase implementation plan with task checklists, written before BMAD was installed. Per the user's decision, this PRD (and the architecture/epics documents that follow it) supersede `docs/plan.md` as the source of truth going forward — treat it as historical reference only once `bmad-create-epics-and-stories` produces its own epic/story breakdown.

## Full Source Specification
The complete original technical specification (90 sections: domain model field-by-field, API route list, LangGraph node-by-node pipeline design, repository directory structure, coding standards, etc.) lives in `Idea.MD` at the repo root and remains the most detailed reference for the architecture phase.
