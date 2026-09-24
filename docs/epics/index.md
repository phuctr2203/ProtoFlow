---
stepsCompleted: [1, 2]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-IdeaForge-2026-09-17/prd.md
  - _bmad-output/planning-artifacts/prds/prd-IdeaForge-2026-09-17/addendum.md
  - Idea.MD
  - docs/plan.md
---

# ProtoFlow - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for ProtoFlow, decomposing the requirements from the PRD and the technical/architecture-equivalent content in `addendum.md` and `Idea.MD` into implementable stories. No formal Architecture.md or UX design contract exists yet; `addendum.md` and `Idea.MD` serve as the technical-decisions input in their place.

## Requirements Inventory

### Functional Requirements

FR1: Receive a meeting-completion ("transcript ready") notification and acknowledge it in under 2 seconds, deferring all processing to the background.
FR2: Retrieve a Meeting's raw transcript and normalize it into speaker-attributed, timestamped segments.
FR3: Simulate meeting-completion events using pre-built transcripts covering a range of realistic transcript quality (at least 5 distinct noise profiles), each flowing through the full pipeline without manual intervention.
FR4: Extract the client's business context, problem, and desired outcomes from a transcript, distinguishing stated business impact from ProtoFlow's own interpretation.
FR5: Extract functional and non-functional requirements from a transcript, each carrying an EXPLICIT/INFERRED marking, a priority, and either supporting Evidence (quote, speaker, timestamp) or a NEEDS_REVIEW status.
FR6: Extract user personas/roles, technical/regulatory constraints, decisions explicitly made, risks, unresolved open questions, and action items (with owner/deadline where mentioned).
FR7: Validate that every important extracted item's Evidence exists, actually supports the claim, has a correctly attributed speaker and timestamp, and that inferred items are marked as such; flag weak evidence as NEEDS_REVIEW.
FR8: Generate an MVP Specification (objective, target users, core user journey, candidate features, acceptance criteria, demo scenario) from Meeting Intelligence, classifying every feature as MUST_HAVE/SHOULD_HAVE/NICE_TO_HAVE/OUT_OF_SCOPE and actively excluding non-essential features.
FR9: Version each MVP Specification; never overwrite an already-approved version.
FR10: Allow a consultant to Approve, Reject, Edit, or Request Revision on a proposed MVP Specification version, persisting who/when/comments.
FR11: Prevent Design and Development from starting on a Project until it has an approved MVP Specification version (refused, not silently allowed).
FR12: Generate the user journey, screen list, navigation, and key UI states for an approved MVP.
FR13: Generate a lightweight technical design (components, APIs, data model, AI workflow, key technology decisions) for an approved MVP, scaled to roughly 1-5 pages equivalent, requiring no manual intervention.
FR14: Break an approved, designed MVP into an ordered set of development tasks.
FR15: Have development agents inspect the existing repository, implement the designed MVP, write accompanying tests, and open a pull request for human review, executing generated code only in an isolated environment and never auto-merging/deploying.
FR16: Generate test cases from the MVP's requirements and acceptance criteria, execute them, and record pass/fail with evidence.
FR17: Report, per requirement, whether it is covered by at least one test, rolling up into overall coverage and pass/fail counts; every MUST_HAVE requirement has at least one mapped test before a Project can be marked demo-ready.
FR18: Generate a demo objective, step-by-step demo script, and synthetic demo data (clearly marked as synthetic) for a validated MVP.
FR19: Label every capability shown in a demo as IMPLEMENTED, SIMULATED, or NOT_IMPLEMENTED, ensuring the demo script and demo package agree and never presenting simulated functionality as production functionality.
FR20: Let a consultant view, per Project, the current stage and status of Meeting, MVP, Design, Development, QA, and Demo at a glance.

### NonFunctional Requirements

NFR1 (Performance): Notification/webhook handling responds in under 2 seconds; all AI processing is asynchronous, never inline in the request/webhook path.
NFR2 (Reliability): Every asynchronous job (transcript processing, intelligence extraction, MVP analysis, design, code generation, QA, demo prep) has a PENDING/RUNNING/COMPLETED/FAILED lifecycle with retry and a surfaced error reason (job ID, error message, timestamp, attempt count).
NFR3 (Idempotency): The same meeting-completion notification, delivered more than once, results in processing exactly once (idempotency key = provider + external_event_id).
NFR4 (Auditability): Structured (JSON) logs exist for every major processing event — what happened, for which project/meeting, how long it took, what was produced.
NFR5 (Security): Generated/untrusted code never executes outside an isolated environment (never directly in the main app process); secrets are never committed, logged, or exposed.
NFR6 (Configurability): Confidence thresholds for high/medium/needs-review are configurable, not hardcoded.
NFR7 (Scope discipline): MVP Specification output size targets "small enough to demo," not "complete enough to build the full product" — a design constraint on the AI's proposal, not just a UI limit.
NFR8 (Privacy): [ASSUMPTION] v1 is single-operator/self-hosted/dev; sensitive transcript data is managed by keeping data local rather than by formal access-control features.
NFR9 (Cost/Portability): [ASSUMPTION] No LLM budget/quota enforcement required at v1 scale, but the LLM access layer must not make provider switching (e.g. to a cheaper model) require rework.

### Additional Requirements

- **Open architectural decision (highest risk):** how development agents actually generate code — a custom tool-use loop vs. wrapping an existing coding-agent engine (Claude Agent SDK, Aider, OpenHands) — is unresolved and deserves a dedicated spike before the AI-Assisted Development epic is built (PRD §11, Idea.MD §67 note).
- **LLM access:** a custom `LLMProvider` abstraction (`backend/app/ai/llm/`), deliberately not relying directly on LangChain's chat-model interface, so provider/framework can be swapped later; config-driven provider selection via `LLM_PROVIDER` env var; built on LangGraph for agent orchestration.
- **Job queue:** Arq (async, Redis-backed) — chosen over Celery (too heavy) and RQ (sync-only).
- **Database:** PostgreSQL as system of record, SQLAlchemy 2.0 (async) + Alembic migrations, managed via `uv` (backend) / `npm` (frontend).
- **Vector DB / object storage timing:** Qdrant and MinIO (local)/Azure Blob (future) are introduced only at the AI-Assisted Development epic, when the generated sample MVP first needs retrieval/document storage — not before.
- **Observability:** structured logs from the start; LangSmith tracing turned on from the Meeting Intelligence epic onward.
- **Docker Compose service introduction timing:** Foundation ships only `postgres`, `redis`, `backend`, `frontend`; `worker` (Arq) is added at Meeting Integration; `qdrant`, `minio` are added at AI-Assisted Development.
- **Meeting provider abstraction:** a `MeetingProvider` Protocol (`get_meeting`, `get_transcript`, `verify_webhook`) decouples business logic from any specific platform; v1 ships only `MockMeetingProvider`. Real integration (leaning self-hosted Jitsi+Jigasi over JaaS/8x8, not yet committed) is explicitly deferred past v1.
- **Mock transcript fixtures:** ~5 fixtures built around one shared "document Q&A assistant" client scenario, each with a distinct noise profile — clean, ASR-noisy (word-level errors), diarization-noisy (wrong/missing speaker attribution), mixed-language (e.g. Vietnamese/English), and one combined profile. These double as the AI evaluation dataset (precision/recall/faithfulness/evidence accuracy).
- **Repository structure:** backend (`app/api/v1`, `core`, `db/models`+`migrations`, `domain/{projects,meetings,intelligence,mvp,design,development,qa,demo}`, `ai/{llm,graphs,agents,prompts,schemas,evaluation}`, `integrations/{meetings,github,storage}`, `workers`, `tests`); frontend (`src/{app,components,pages,features,hooks,services,types,lib}`); `infrastructure/{docker,scripts}`; `docs/`.
- **API surface:** REST under `/api/v1/` — `projects`, `projects/{id}/meetings`, `meetings/{id}`, `meetings/{id}/transcript`, `meetings/{id}/intelligence`, `projects/{id}/mvp` (+ `/approve`), `projects/{id}/design`, `projects/{id}/development` (+ `/tasks`), `projects/{id}/qa`, `projects/{id}/demo`; webhook `POST /api/v1/webhooks/jitsi`.
- **Core domain models:** `Project` (status enum DISCOVERY→...→COMPLETED), `Meeting` (status enum incl. TRANSCRIPT_READY), `Transcript` + `TranscriptSegment`, `MeetingEvent` (idempotency key = provider + external_event_id), `ProcessingJob` (job_type enum: TRANSCRIPT_PROCESSING, MEETING_INTELLIGENCE, MVP_ANALYSIS, MVP_DESIGN, CODE_GENERATION, QA, DEMO_PREPARATION), `MeetingIntelligenceState` (LangGraph TypedDict), `Requirement`/`Evidence`/`Persona`/`Constraint`/`Decision`/`Risk`/`OpenQuestion`/`ActionItem` (Pydantic, structured outputs only — no free-form LLM output for system-critical objects), `MVPSpecification`, `MVPApproval`.
- **Meeting Intelligence pipeline (LangGraph):** preprocessing → segmentation → business context → requirements → personas → constraints → decisions → open questions → risks → evidence validation → synthesis.
- **MVP Definition agent team:** Product Manager, Feature Analyst, UX Analyst, Scope Analyst, Critic, Synthesizer.
- **Architecture principles:** domain-first (API routes stay thin → Application Service → Domain → AI/Infrastructure, not business logic embedded in routes); provider abstraction for both meetings and LLMs; async processing for all long-running AI work; structured (Pydantic) outputs; source traceability on AI-generated artifacts; human approval gates; version everything important (MVP spec, prompts, AI outputs, design, generated code/task plans).
- **Prompt management:** prompts stored separately from application logic under `ai/prompts/`, one file per pipeline node, versioned/traceable.
- **Coding standards:** Python — ruff, black, mypy where practical, pytest. TypeScript — ESLint, Prettier, strict mode. Small modules, clear naming, no large monolithic files.
- **Testing strategy:** backend — pytest covering API, DB, domain logic, agent schemas, workflow, webhook, event idempotency. Frontend — components, page flows, API integration, approval flow. AI — maintain a small (10-30 transcript) evaluation dataset tracking precision/recall/faithfulness/evidence accuracy; the 5 mock transcript fixtures seed this dataset.
- **GitHub integration:** branch + PR creation for generated code; nothing auto-merged or auto-deployed.
- **Definition of Done (every feature):** implementation exists, tests exist, error handling exists, logs exist, API documented, UI usable, DB migration exists if required, no secrets committed, acceptance criteria satisfied.
- **Standing rules (every phase):** no out-of-scope features slip in (pricing, estimation, resourcing, full PM, k8s, etc.); inferred requirements never presented as confirmed; requirement traceability maintained; structured outputs for all AI-critical data; long-running AI work stays in async jobs; webhook/event processing stays idempotent.
- **Suggested build order / incrementality constraint:** build the pipeline incrementally, in dependency order (repo/Docker → backend/DB/frontend foundation → project mgmt → meeting model → provider integration → webhook → transcript processing → meeting intelligence → traceability → MVP agent team/UI → human approval → MVP design → development task generation → GitHub integration → coding agent → QA agent → demo prep → end-to-end integration); do not start by building all agents simultaneously.

### UX Design Requirements

None — no UX design contract (`DESIGN.md`/`EXPERIENCE.md`) exists for this project yet.

### FR Coverage Map

Each phase from [`docs/plan.md`](../plan.md) becomes one epic (Epic N ↔ Phase N). Epic 0
(Foundation) carries no FR of its own — it's the base every other epic builds on and delivers the
Project Workspace shell that FR-20 is later completed against in Epic 9.

| FR | Requirement (short) | Epic |
|---|---|---|
| FR-1 | Receive meeting-completion notification (<2s, deferred) | [Epic 1](epic-01-meeting-integration.md) |
| FR-2 | Retrieve & normalize transcript into segments | [Epic 1](epic-01-meeting-integration.md) |
| FR-3 | Simulate meetings via mock provider (5 noise profiles) | [Epic 1](epic-01-meeting-integration.md) |
| FR-4 | Extract business context, problem, goals | [Epic 2](epic-02-meeting-intelligence.md) |
| FR-5 | Extract requirements with evidence / NEEDS_REVIEW | [Epic 2](epic-02-meeting-intelligence.md) |
| FR-6 | Extract personas, constraints, decisions, risks, questions, actions | [Epic 2](epic-02-meeting-intelligence.md) |
| FR-7 | Validate extracted evidence | [Epic 2](epic-02-meeting-intelligence.md) |
| FR-8 | Propose a scoped MVP | [Epic 3](epic-03-mvp-definition.md) |
| FR-9 | Version MVP specifications | [Epic 3](epic-03-mvp-definition.md) |
| FR-10 | Approve / reject / edit / request revision | [Epic 4](epic-04-human-approval.md) |
| FR-11 | Block downstream phases until approval | [Epic 4](epic-04-human-approval.md) |
| FR-12 | Generate UX flow & screen definitions | [Epic 5](epic-05-mvp-design.md) |
| FR-13 | Generate lightweight technical design | [Epic 5](epic-05-mvp-design.md) |
| FR-14 | Break MVP into implementation tasks | [Epic 6](epic-06-ai-development.md) |
| FR-15 | Implement MVP against a real repository (PR) | [Epic 6](epic-06-ai-development.md) |
| FR-16 | Generate & execute test cases from requirements | [Epic 7](epic-07-qa.md) |
| FR-17 | Report requirement coverage | [Epic 7](epic-07-qa.md) |
| FR-18 | Generate a demo package | [Epic 8](epic-08-demo-preparation.md) |
| FR-19 | Honestly represent implementation status | [Epic 8](epic-08-demo-preparation.md) |
| FR-20 | View project status across all phases | [Epic 9](epic-09-end-to-end-demo.md) (workspace shell begun in [Epic 0](epic-00-foundation.md)) |

**NFR placement:** NFR1–NFR4 (performance, reliability, idempotency, auditability) are established
in [Epic 1](epic-01-meeting-integration.md); NFR6 (configurable confidence) and NFR9 (provider
portability) in [Epic 2](epic-02-meeting-intelligence.md); NFR7 (MVP scope discipline) in
[Epic 3](epic-03-mvp-definition.md); NFR5 (isolated code execution) in
[Epic 6](epic-06-ai-development.md). NFR8 (privacy / local-data-only) is a standing v1 posture, not
a build task.

## Epic List

Epics are worked **in order** — do not start an epic until the previous epic's Definition of Done is
met (incremental pipeline, Idea.MD §83/§88).

| Epic | Title | Phase | FRs | Depends on |
|---|---|---|---|---|
| [0](epic-00-foundation.md) | Foundation | 0 | — (enables FR-20) | — |
| [1](epic-01-meeting-integration.md) | Meeting Integration | 1 | FR-1, FR-2, FR-3 | 0 |
| [2](epic-02-meeting-intelligence.md) | Meeting Intelligence | 2 | FR-4, FR-5, FR-6, FR-7 | 1 |
| [3](epic-03-mvp-definition.md) | MVP Definition | 3 | FR-8, FR-9 | 2 |
| [4](epic-04-human-approval.md) | Human Approval | 4 | FR-10, FR-11 | 3 |
| [5](epic-05-mvp-design.md) | MVP Design | 5 | FR-12, FR-13 | 4 |
| [6](epic-06-ai-development.md) | AI-Assisted Development | 6 | FR-14, FR-15 | 5 |
| [7](epic-07-qa.md) | Automated QA | 7 | FR-16, FR-17 | 6 |
| [8](epic-08-demo-preparation.md) | Demo Preparation | 8 | FR-18, FR-19 | 7 |
| [9](epic-09-end-to-end-demo.md) | End-to-End Demo | 9 | FR-20 (validates SM-1) | 8 |

## Definition of Done (every feature, Idea.MD §79)

- Implementation exists
- Tests exist
- Error handling exists
- Logs exist
- API documented (OpenAPI auto-docs reviewed)
- UI usable
- DB migration exists if required
- No secrets committed
- Acceptance criteria satisfied

## Standing rules, every epic (Idea.MD §88)

- No out-of-scope features slip in (pricing, estimation, resourcing, full PM, k8s, etc. — PRD §6).
- Inferred requirements never presented as confirmed.
- Requirement traceability maintained.
- Structured (Pydantic) outputs for all AI-critical data.
- Long-running AI work stays in async jobs, never inline in a request/webhook.
- Webhook/event processing stays idempotent.
