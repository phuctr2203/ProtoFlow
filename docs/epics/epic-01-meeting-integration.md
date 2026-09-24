---
epic: 1
title: Meeting Integration
phase: 1
status: In Progress
depends_on: [0]
fr_covered: [FR-1, FR-2, FR-3]
nfr_covered: [NFR1, NFR2, NFR3, NFR4]
sources:
  - Idea.MD §9, §10, §11, §12, §48, §49, §50, §62, §72
  - docs/plan.md Phase 1
  - PRD §5.1, addendum (mock fixtures, provider abstraction, service timing)
---

# Epic 1 — Meeting Integration

## Goal

A simulated meeting-completion event flows automatically through webhook → event store → queue →
worker → `Meeting.status = TRANSCRIPT_READY`, with no real meeting platform involved. This proves
the asynchronous, idempotent ingestion backbone that every AI phase runs on.

## Dependencies

Epic 0 (Foundation).

## Key decisions (this epic)

- Build against `MockMeetingProvider` only. Real Jitsi/JaaS integration is deferred past v1
  (leaning self-hosted Jitsi+Jigasi, not committed — PRD §7.2, addendum).
- 5 mock transcript fixtures around the shared "document Q&A assistant" scenario (Idea.MD §71),
  each a distinct noise profile: clean, ASR-noisy, diarization-noisy, mixed-language (VN/EN),
  combined. These double as the AI eval dataset used from Epic 2 on.
- Arq introduced here (first real background job). Transcript raw/normalized text stored as
  Postgres columns — no object storage yet.

## Stories

### Story 1.1 — Meeting provider abstraction (FR-3)
**As** the builder, **I want** a provider interface with a mock implementation, **so that** the
pipeline can run without a real meeting platform and a real one can be added later untouched.

**Acceptance criteria:**
- `MeetingProvider` Protocol with `get_meeting`, `get_transcript`, `verify_webhook` (Idea.MD §48).
- `MockMeetingProvider` implements it.
- No downstream code depends on a concrete provider.

### Story 1.2 — Mock transcript fixtures (FR-3)
**As** the builder, **I want** realistic transcript fixtures of varying quality, **so that**
evidence validation and confidence scoring are exercised beyond a clean happy path.

**Acceptance criteria:**
- At least 5 fixtures exist, each with a distinct noise profile (clean, ASR-noisy,
  diarization-noisy, mixed-language, combined).
- All are built around the shared document-Q&A client scenario.
- Every fixture flows through the full pipeline without manual intervention.

### Story 1.3 — Meeting & Transcript models (FR-2)
**As** a consultant, **I want** Meetings and their transcripts persisted with speaker-attributed
segments, **so that** intelligence extraction has structured input.

**Acceptance criteria:**
- `Meeting` model with status enum incl. `TRANSCRIPT_READY` (Idea.MD §9) + migration.
- `Transcript` and `TranscriptSegment` models (Idea.MD §10) + migration.
- Each segment carries speaker, start time, end time, text.

### Story 1.4 — Idempotent meeting events (FR-1, NFR3)
**As** the builder, **I want** inbound events deduplicated, **so that** a redelivered notification
never double-processes.

**Acceptance criteria:**
- `MeetingEvent` model + migration with idempotency key = `provider + external_event_id`
  (Idea.MD §11).
- The same event delivered twice is processed exactly once.

### Story 1.5 — Processing job lifecycle (NFR2)
**As** the builder, **I want** every async job to have an explicit lifecycle and error surface,
**so that** failures are visible and retryable.

**Acceptance criteria:**
- `ProcessingJob` model + migration with job types (Idea.MD §12) and `PENDING`/`RUNNING`/
  `COMPLETED`/`FAILED` states.
- Failed jobs expose job ID, error message, timestamp, attempt count (Idea.MD §76).

### Story 1.6 — Lightweight webhook (FR-1, NFR1)
**As** the builder, **I want** the webhook to validate, persist, enqueue, and return fast, **so
that** long AI work never runs inline.

**Acceptance criteria:**
- `POST /api/v1/webhooks/jitsi` validates → persists event → enqueues job → returns 200.
- Response is under 2 seconds; no LLM/processing runs inline (Idea.MD §49, §72).

### Story 1.7 — Worker & queue wiring (NFR2)
**As** the builder, **I want** an Arq worker consuming Redis jobs, **so that** enqueued work is
processed out of band.

**Acceptance criteria:**
- Arq worker skeleton + Redis wiring.
- `worker` service added to `docker-compose.yml`.

### Story 1.8 — Transcript processing job (FR-2, NFR2)
**As** the builder, **I want** a job that fetches and normalizes a transcript and advances Meeting
status, **so that** a completed meeting becomes ready automatically.

**Acceptance criteria:**
- Job fetches the transcript via the provider, normalizes it, and advances `Meeting.status` to
  `TRANSCRIPT_READY`.
- Retry and failure handling populate `attempt_count` / `error_message`.

### Story 1.9 — Local meeting simulation (FR-3)
**As** the builder, **I want** to trigger a simulated meeting + event locally, **so that** I can
drive the pipeline without external systems.

**Acceptance criteria:**
- A dev-only endpoint or script simulates a meeting and emits a webhook event for a chosen fixture.

### Story 1.10 — Meetings page (FR-20 partial)
**As** a consultant, **I want** to see meetings and their statuses, **so that** I can track
ingestion progress.

**Acceptance criteria:**
- Meetings page lists meetings with title, date, participants, transcript status, processing status
  (Idea.MD §40).

## Epic Definition of Done

- Simulating a meeting drives `Meeting.status` to `TRANSCRIPT_READY` automatically.
- Duplicate webhook delivery does not double-process.
- All 5 mock transcripts flow through cleanly.
- Tests cover webhook idempotency and end-to-end processing of all 5 fixtures.
- Tests pass; standing rules honored (see [index.md](index.md)).
