# ProtoFlow Delivery Plan

> Companion to [`Idea.MD`](../Idea.MD) (the full spec). This document turns that spec into an
> execution plan: phases, in dependency order, each with a task checklist and a Definition of
> Done. Architecture decisions referenced here were made in project discussion and are also kept
> in Claude's project memory (`protoflow-architecture-decisions`).

## How to use this plan

- Phases mirror Idea.MD §61–§70 (Phase 0–9) and the milestone strategy (§84).
- Work phases **in order**. Do not start a phase until the previous phase's Definition of Done
  is checked off — per Idea.MD §83/§88: build the pipeline incrementally, not all agents at once.
- Check off tasks (`- [ ]` → `- [x]`) as they're completed. Update each phase's **Status** line.
- If a task turns out to need a decision not covered here, stop and raise it rather than guessing
  (Idea.MD §88 Rule 2, and CLAUDE.md).

**Status legend:** `Not Started` · `In Progress` · `Blocked` · `Done`

| Phase | Title | Status |
|---|---|---|
| 0 | Foundation | Not Started |
| 1 | Meeting Integration | Not Started |
| 2 | Meeting Intelligence | Not Started |
| 3 | MVP Definition | Not Started |
| 4 | Human Approval | Not Started |
| 5 | MVP Design | Not Started |
| 6 | AI Development | Not Started |
| 7 | QA | Not Started |
| 8 | Demo Preparation | Not Started |
| 9 | End-to-End Demo | Not Started |

---

## Phase 0 — Foundation

**Status:** Not Started
**Depends on:** nothing
**Goal:** A running skeleton — Docker Compose brings up backend + frontend + Postgres, you can
create a Project through the UI and see it persisted. No AI, no meetings yet.

**Decisions for this phase:**
- Docker Compose starts with only `postgres`, `redis`, `backend`, `frontend`. `worker` (Arq) is
  added in Phase 1 when there's an actual job to run. `qdrant` and `minio` are added in Phase 6
  when the generated sample MVP first needs vector search / file storage — not before.
- Backend managed with `uv`. Frontend with `npm`.

**Tasks:**
- [ ] Repo skeleton per Idea.MD §58 (`backend/`, `frontend/`, `infrastructure/`, `docs/`)
- [ ] Backend: FastAPI app skeleton (`uv`-managed `pyproject.toml`)
- [ ] Backend: `core/config.py` — Pydantic Settings reading `.env`
- [ ] Backend: `core/logging.py` — structured (JSON) logging
- [ ] Backend: `db/database.py` — async SQLAlchemy engine/session
- [ ] Backend: `Project` SQLAlchemy model + first Alembic migration (§8)
- [ ] Backend: `Project` Pydantic schemas (Create/Read)
- [ ] Backend: `domain/projects/service.py` application service — API routes must stay thin
  (Architecture Principle 1, §81)
- [ ] Backend: `/api/v1/projects` endpoints (create, list, get)
- [ ] Backend: `/health` endpoint
- [ ] Backend: pytest scaffold + first passing test
- [ ] Frontend: Vite + React + TS + Tailwind + shadcn/ui scaffold
- [ ] Frontend: React Query + API client/service layer
- [ ] Frontend: basic Project list + create UI (Project Workspace shell, §38)
- [ ] Infra: `docker-compose.yml` (postgres, redis, backend, frontend)
- [ ] Infra: `.env.example`
- [ ] Infra: `Makefile` (up / down / migrate / test)
- [ ] `README.md` with local dev setup instructions

**Definition of Done:**
- [ ] `docker compose up` starts every service successfully (§61 acceptance)
- [ ] A Project can be created via the UI and is persisted in Postgres
- [ ] `/health` returns 200
- [ ] Tests pass
- [ ] No secrets committed; `.env.example` accurate

---

## Phase 1 — Meeting Integration

**Status:** Not Started
**Depends on:** Phase 0
**Goal:** A simulated meeting completion event flows automatically through webhook → queue →
worker → `Meeting.status = TRANSCRIPT_READY`, with no real Jitsi involved yet.

**Decisions for this phase:**
- Build against `MockMeetingProvider` only. Real Jitsi/JaaS integration is a later, isolated
  swap-in (leaning self-hosted Jitsi+Jigasi eventually, per project decisions — not now).
- 5 mock transcript fixtures, reusing the spec's own simple document-Q&A client scenario
  (§71), each with a different noise profile: clean, ASR-noisy (fast/unclear speech → word
  errors), diarization-noisy (wrong/missing speaker attribution), mixed-language
  (Vietnamese/English), and one combining two of the above.
- Arq introduced here (first real background job). Transcript raw/normalized text stored as
  Postgres columns — no object storage needed yet.

**Tasks:**
- [ ] Backend: `MeetingProvider` Protocol (§48)
- [ ] Backend: `MockMeetingProvider` implementation
- [ ] Backend: 5 mock transcript fixtures (see noise profiles above)
- [ ] Backend: `Meeting` model + migration (§9)
- [ ] Backend: `Transcript` + `TranscriptSegment` models + migration (§10)
- [ ] Backend: `MeetingEvent` model + migration; idempotency key = `provider + external_event_id`
  (§11)
- [ ] Backend: `ProcessingJob` model + migration (§12)
- [ ] Backend: `POST /api/v1/webhooks/jitsi` — validate → persist event → enqueue job → return
  200, **under 2 seconds, no LLM/processing inline** (§49, §72)
- [ ] Backend: Arq worker skeleton + Redis wiring; add `worker` service to `docker-compose.yml`
- [ ] Backend: transcript processing job — fetch via provider, normalize, advance Meeting status
- [ ] Backend: job retry/failure handling (`attempt_count`, `error_message`)
- [ ] Backend: dev-only endpoint/script to simulate a meeting + webhook event locally
- [ ] Frontend: Meetings page — list + statuses (§40)
- [ ] Tests: webhook idempotency (same event delivered twice → processed once)
- [ ] Tests: all 5 mock transcripts process end-to-end without error

**Definition of Done:**
- [ ] Simulating a meeting drives `Meeting.status` to `TRANSCRIPT_READY` automatically
- [ ] Duplicate webhook delivery does not double-process
- [ ] All 5 mock transcripts flow through cleanly
- [ ] Tests pass

---

## Phase 2 — Meeting Intelligence

**Status:** Not Started
**Depends on:** Phase 1
**Goal:** Given a transcript, produce structured Meeting Intelligence (business context,
requirements, personas, constraints, decisions, risks, open questions, action items), every
important requirement carrying evidence or an explicit `INFERRED`/`NEEDS_REVIEW` marking.

**Decisions for this phase:**
- Custom `LLMProvider` abstraction layer built here (first real LLM usage) — the layer that
  lets us swap providers/frameworks later without touching callers.
- LangGraph pipeline per §16/§51. LangSmith tracing turned on from this phase forward.

**Tasks:**
- [ ] Backend: `LLMProvider` abstraction (`ai/llm/`) + one concrete OpenAI-compatible
  implementation
- [ ] Backend: config-driven provider selection (`LLM_PROVIDER` env var)
- [ ] Backend: Pydantic schemas — `BusinessContext`, `Requirement`, `Persona`, `Constraint`,
  `Decision`, `Risk`, `OpenQuestion`, `ActionItem`, `Evidence` (§13, §53)
- [ ] Backend: `MeetingIntelligenceState` TypedDict (§52)
- [ ] Backend: LangGraph nodes — preprocessing, segmentation, business context, requirements,
  personas, constraints, decisions, open questions, risks (§16)
- [ ] Backend: Evidence Validator node — evidence exists & supports the requirement, speaker
  attributed, timestamp present, `EXPLICIT` vs `INFERRED` marked, confidence assigned, weak
  evidence → `NEEDS_REVIEW` (§15, §17)
- [ ] Backend: Meeting Intelligence Synthesizer node
- [ ] Backend: `MEETING_INTELLIGENCE` job type wired into worker
- [ ] Backend: `ai/prompts/meeting_intelligence/` — one prompt file per node (§55)
- [ ] Backend: `GET /api/v1/meetings/{id}/intelligence`
- [ ] Frontend: Intelligence page — all sections, evidence display, confidence (§41)
- [ ] AI eval: run all 5 mock transcripts through the pipeline; manually verify extraction
  (seeds the eval dataset for §78)
- [ ] Confirm LangSmith traces are visible for a full pipeline run

**Definition of Done:**
- [ ] Each of the 5 mock transcripts produces intelligence with evidence per requirement, or an
  explicit `NEEDS_REVIEW`/`INFERRED` marking
- [ ] Noisy transcripts produce lower confidence / `NEEDS_REVIEW`, not false-confident output
- [ ] Tests pass

---

## Phase 3 — MVP Definition

**Status:** Not Started
**Depends on:** Phase 2
**Goal:** Given Meeting Intelligence, produce a deliberately small `MVPSpecification` — not a
full enterprise PRD.

**Tasks:**
- [ ] Backend: `MVPSpecification` schema (§19)
- [ ] Backend: agent nodes — Product Manager, Feature Analyst, UX Analyst, Scope Analyst,
  Critic, Synthesizer (§18, §51)
- [ ] Backend: scope classification enum — `MUST_HAVE` / `SHOULD_HAVE` / `NICE_TO_HAVE` /
  `OUT_OF_SCOPE` (§21)
- [ ] Backend: `MVP_ANALYSIS` job type
- [ ] Backend: MVP versioning — never overwrite an approved version (§23)
- [ ] Backend: `GET/POST /api/v1/projects/{id}/mvp`
- [ ] Frontend: MVP page (§42) — objective, users, journey, features, scope buckets,
  assumptions, open questions, acceptance criteria, demo scenario
- [ ] AI eval: run all 5 mock transcripts through; sanity-check the MVP stays small each time

**Definition of Done:**
- [ ] For the document-Q&A mock scenario, the generated MVP matches the spirit of §20/§71
  (small, demoable, not the full feature list)
- [ ] Tests pass

---

## Phase 4 — Human Approval

**Status:** Not Started
**Depends on:** Phase 3
**Goal:** MVP definition cannot silently proceed to design/development.

**Tasks:**
- [ ] Backend: `MVPApproval` model + migration (§22)
- [ ] Backend: `POST /api/v1/projects/{id}/mvp/approve` (approve / reject / request revision)
- [ ] Backend: hard guard — Design/Development cannot start without an approved MVP version
- [ ] Frontend: Approve / Reject / Edit / Request Revision actions on the MVP page

**Definition of Done:**
- [ ] Starting Design without an approved MVP is blocked
- [ ] Approval persisted with version, approver, timestamp, comments
- [ ] Tests pass

---

## Phase 5 — MVP Design

**Status:** Not Started
**Depends on:** Phase 4
**Goal:** Lightweight UX flow + technical design from an approved MVP — target 1–5 pages
equivalent, not a huge architecture document (§26).

**Tasks:**
- [ ] Backend: UX Agent — user journey, screens, navigation, key states (§25)
- [ ] Backend: Solution Design Agent — components, APIs, data model, AI workflow, tech
  decisions (§26)
- [ ] Backend: `MVP_DESIGN` job type
- [ ] Backend: `GET /api/v1/projects/{id}/design`
- [ ] Frontend: Design page (§43)

**Definition of Done:**
- [ ] Design generates from an approved MVP without manual intervention
- [ ] Output stays lightweight
- [ ] Tests pass

---

## Phase 6 — AI Development

**Status:** Not Started
**Depends on:** Phase 5
**Goal:** Generate working code for the MVP against a real GitHub repo.

**⚠ Open decision — resolve before starting this phase:** how the coding agents actually work
(custom tool-use loop vs. wrapping an existing engine such as the Claude Agent SDK/Claude Code,
Aider, or OpenHands behind our own Development Manager). This is the single riskiest unknown in
the whole spec and deserves its own focused discussion, not an assumption baked into this plan.

**Decisions for this phase:**
- `qdrant` and `minio` are added to Docker Compose here — first genuine need (RAG for the
  generated document-Q&A MVP, and document/artifact storage).

**Tasks:**
- [ ] Decide coding-agent approach (separate discussion — see note above)
- [ ] Backend: Development Manager — task breakdown from MVP spec (§28, §30)
- [ ] Backend: repository inspection step (must understand existing code before writing more,
  §31 Rule 1)
- [ ] Backend: Frontend/Backend/AI Engineer agent roles (shape depends on the decision above)
- [ ] Backend: GitHub integration — branch + PR creation (§27, §32)
- [ ] Infra: add `qdrant`, `minio` services
- [ ] Backend: `CODE_GENERATION` job type
- [ ] Backend: isolated execution environment for generated code — never run untrusted
  generated code in the main app process (§72)

**Definition of Done:**
- [ ] Working code generated for the document-Q&A sample MVP; a GitHub PR is opened
- [ ] Generated code only ever executes in the isolated environment
- [ ] Tests pass (generated + our own)

---

## Phase 7 — QA

**Status:** Not Started
**Depends on:** Phase 6
**Goal:** Validate the generated MVP against requirements and acceptance criteria.

**Tasks:**
- [ ] Backend: QA Agent — generate test cases from requirements/acceptance criteria (§33)
- [ ] Backend: test execution + PASS/FAIL/evidence capture
- [ ] Backend: Requirement → Feature → Task → Code → Test traceability (§34)
- [ ] Backend: `QA` job type
- [ ] Frontend: QA page (§45)

**Definition of Done:**
- [ ] QA report shows requirement coverage % and pass/fail counts
- [ ] Every `MUST_HAVE` requirement has at least one mapped test
- [ ] Tests pass

---

## Phase 8 — Demo Preparation

**Status:** Not Started
**Depends on:** Phase 7
**Goal:** Package the working MVP for an honest client demo.

**Tasks:**
- [ ] Backend: Demo Agent — objective, script, data, implemented/simulated/not-implemented
  breakdown (§35–§37)
- [ ] Backend: synthetic demo data generation, clearly marked as synthetic (§36)
- [ ] Backend: `DEMO_PREPARATION` job type
- [ ] Frontend: Demo page + Start Demo action (§46)

**Definition of Done:**
- [ ] Demo package includes an honest `IMPLEMENTED` / `SIMULATED` / `NOT_IMPLEMENTED` breakdown
- [ ] Demo script matches what was actually built (no overclaiming, §37)

---

## Phase 9 — End-to-End Demo

**Status:** Not Started
**Depends on:** Phase 8
**Goal:** The full §70/§85 scenario runs start to finish: create project → simulated meeting →
transcript → intelligence → MVP proposal → human approval → design → generated code → QA →
working MVP → demo package.

**Tasks:**
- [ ] Full walkthrough executed manually, end to end
- [ ] Fix any integration gaps found
- [ ] Document the working demo

**Definition of Done:**
- [ ] The full success scenario completes without manual data-fixing along the way

---

## Appendix A — Definition of Done template (applies to every phase, §79)

- [ ] Implementation exists
- [ ] Tests exist
- [ ] Error handling exists
- [ ] Logs exist
- [ ] API documented (OpenAPI auto-docs reviewed)
- [ ] UI usable
- [ ] DB migration exists if required
- [ ] No secrets committed
- [ ] Acceptance criteria satisfied

## Appendix B — Standing rules, every phase (§88)

- [ ] No out-of-scope features slipped in (pricing, estimation, resourcing, full PM, k8s, etc. —
  §3.2)
- [ ] Inferred requirements never presented as confirmed
- [ ] Requirement traceability maintained
- [ ] Structured (Pydantic) outputs for all AI-critical data
- [ ] Long-running AI work stays in async jobs, never inline in a request/webhook
- [ ] Webhook/event processing stays idempotent
