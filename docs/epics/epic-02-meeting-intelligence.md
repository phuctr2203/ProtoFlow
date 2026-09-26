---
epic: 2
title: Meeting Intelligence
phase: 2
status: In Progress
depends_on: [1]
fr_covered: [FR-4, FR-5, FR-6, FR-7]
nfr_covered: [NFR6, NFR9]
sources:
  - Idea.MD §13, §14, §15, §16, §17, §51, §52, §53, §54, §55, §63
  - docs/plan.md Phase 2
  - PRD §5.2, addendum (LLMProvider, LangSmith)
---

# Epic 2 — Meeting Intelligence

## Goal

Given a transcript, produce structured Meeting Intelligence — business context, requirements,
personas, constraints, decisions, risks, open questions, action items — where every important
requirement carries Evidence or an explicit `INFERRED` / `NEEDS_REVIEW` marking, never blended
silently.

## Dependencies

Epic 1 (Meeting Integration).

## Key decisions (this epic)

- Custom `LLMProvider` abstraction built here (first real LLM usage), deliberately not relying
  directly on LangChain's chat-model interface, so provider/framework can be swapped later (NFR9,
  addendum).
- LangGraph pipeline per Idea.MD §16/§51. LangSmith tracing on from this epic forward.
- All system-critical AI outputs are structured Pydantic objects — no free-form text (Idea.MD §53).

## Stories

### Story 2.1 — LLM provider abstraction (NFR9)
**As** the builder, **I want** a config-driven LLM access layer, **so that** switching providers or
models later requires no caller changes.

**Acceptance criteria:**
- `LLMProvider` abstraction under `ai/llm/` with one concrete OpenAI-compatible implementation.
- Provider selection driven by `LLM_PROVIDER` env var.

### Story 2.2 — Structured intelligence schemas (FR-5, FR-6)
**As** the builder, **I want** Pydantic schemas for every extracted item, **so that** outputs are
validated, not free-form.

**Acceptance criteria:**
- Schemas for `BusinessContext`, `Requirement`, `Persona`, `Constraint`, `Decision`, `Risk`,
  `OpenQuestion`, `ActionItem`, `Evidence` (Idea.MD §13, §53).
- `Requirement` carries type, priority, status, `EXPLICIT`/`INFERRED`, `Evidence`, confidence.

### Story 2.3 — Extraction pipeline (FR-4, FR-5, FR-6)
**As** a consultant, **I want** the transcript decomposed into structured project knowledge, **so
that** I can review what the client actually asked for.

**Acceptance criteria:**
- `MeetingIntelligenceState` TypedDict (Idea.MD §52).
- LangGraph nodes: preprocessing, segmentation, business context, requirements, personas,
  constraints, decisions, open questions, risks (Idea.MD §16).
- Business-context output distinguishes stated business impact from ProtoFlow's interpretation
  (FR-4).
- Action items capture owner/deadline where mentioned (FR-6).

### Story 2.4 — Evidence validator (FR-7, NFR6)
**As** a consultant, **I want** every important item's evidence checked, **so that** I never
present my own inference as the client's confirmed scope.

**Acceptance criteria:**
- Validator node verifies: evidence exists and supports the claim, speaker attributed, timestamp
  present, `EXPLICIT` vs `INFERRED` marked, confidence assigned (Idea.MD §15, §17).
- Weak/unsupported evidence → `NEEDS_REVIEW`, not silently accepted or dropped.
- Confidence thresholds (high/medium/needs-review) are configurable, not hardcoded (NFR6).

### Story 2.5 — Synthesis & job wiring
**As** the builder, **I want** the pipeline to run as a background job, **so that** intelligence is
produced asynchronously after a transcript is ready.

**Acceptance criteria:**
- Meeting Intelligence Synthesizer node produces the final structured intelligence.
- `MEETING_INTELLIGENCE` job type wired into the Arq worker.

### Story 2.6 — Prompt management
**As** the builder, **I want** prompts stored separately and versioned, **so that** they're
traceable and editable without touching logic.

**Acceptance criteria:**
- `ai/prompts/meeting_intelligence/` holds one prompt file per node (Idea.MD §55).

### Story 2.7 — Intelligence API & page (FR-20 partial)
**As** a consultant, **I want** to view the extracted intelligence with evidence, **so that** I can
audit each requirement back to the conversation.

**Acceptance criteria:**
- `GET /api/v1/meetings/{id}/intelligence` returns the structured intelligence.
- Intelligence page shows all sections, per-requirement evidence, and confidence (Idea.MD §41).

### Story 2.8 — AI evaluation & tracing (NFR6)
**As** the builder, **I want** the pipeline evaluated against the fixtures, **so that** noisy
transcripts fail safe rather than produce false-confident output.

**Acceptance criteria:**
- All 5 mock transcripts run through the pipeline; extraction is manually verified (seeds the eval
  dataset, Idea.MD §78).
- Noisy transcripts yield lower confidence / `NEEDS_REVIEW`, not false confidence.
- LangSmith traces are visible for a full pipeline run.

### Story 2.9 — Multi-provider LLM support (NFR9) — Done
**As** the builder, **I want** to switch the LLM between the deterministic mock, an OpenAI-compatible
API, and Ollama Cloud via config, **so that** I can run offline, on hosted OpenAI, or on Ollama
without code changes.

**Acceptance criteria:**
- `LLM_PROVIDER` selects `mock` | `openai` | `ollama`; each provider reads its own key/base-url/model
  env vars (`ai/llm/registry.py`, `openai_provider.py`, `ollama_provider.py`).
- Ollama does not honour strict `json_schema` structured output, so the Ollama provider injects the
  schema into the prompt, uses JSON-object mode, strips markdown fences, and retries once before
  failing loudly — producing schema-valid Pydantic objects.
- `docker-compose.yml` passes the provider env through to backend and worker; `.env.example`
  documents every var (no secrets committed).
- Test suite pins the mock provider (autouse fixture) so it never makes real API calls.

### Story 2.10 — LangSmith observability integration — Done
**As** the builder, **I want** the LangGraph chains and the underlying model calls traced to
LangSmith, **so that** I can monitor and debug each pipeline run end to end.

**Acceptance criteria:**
- `LANGSMITH_TRACING` / `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT` / `LANGSMITH_ENDPOINT` configured
  via env and passed through to backend and worker (no key committed).
- The OpenAI/Ollama client is wrapped with `wrap_openai` so each model call is a nested `llm` run
  inside the LangGraph trace; tracing failures never break inference.
- A full meeting-intelligence run produces one root `LangGraph` trace with each node as a child
  chain run and each model call as a child llm run, verified against the LangSmith API.

## Epic Definition of Done

- Each of the 5 mock transcripts produces intelligence with evidence per requirement, or an
  explicit `NEEDS_REVIEW` / `INFERRED` marking.
- Noisy transcripts produce lower confidence / `NEEDS_REVIEW`, not false-confident output.
- Tests pass; standing rules honored (see [index.md](index.md)).
