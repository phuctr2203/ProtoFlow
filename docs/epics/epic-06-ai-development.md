---
epic: 6
title: AI-Assisted Development
phase: 6
status: Not Started
depends_on: [5]
fr_covered: [FR-14, FR-15]
nfr_covered: [NFR5]
sources:
  - Idea.MD §27, §28, §29, §30, §31, §32, §67
  - docs/plan.md Phase 6
  - PRD §5.6, §11 (open question 1), addendum
---

# Epic 6 — AI-Assisted Development

## Goal

Generate working code for the approved, designed MVP against a real GitHub repository, producing a
reviewable pull request. Generated code executes only in an isolated environment; nothing is
auto-merged or auto-deployed.

## Dependencies

Epic 5 (MVP Design).

## ⚠ Open decision — resolve before building

How the development agents actually generate code — a custom tool-use loop vs. wrapping an existing
coding-agent engine (Claude Agent SDK / Claude Code, Aider, OpenHands) behind our own Development
Manager — is unresolved and is the single highest-risk unknown in the product (PRD §11, Idea.MD §67
note). Story 6.0 is a dedicated spike that must complete and be decided before Stories 6.3+ start.

## Key decisions (this epic)

- `qdrant` and `minio` are added to Docker Compose here — first genuine need (RAG for the generated
  document-Q&A MVP, and document/artifact storage) (addendum, service timing).
- The developer team gets its own LLM via `get_dev_llm_provider()` (a separate profile in
  `ai/llm/registry.py`, configured by `DEV_*` env vars), so code-gen and QA can run on a different
  provider/model from the product team. It inherits the shared config until `DEV_*` is set. Dev/QA
  agents (this epic and Epic 7) must resolve their LLM through this accessor, not `get_llm_provider()`.

## Stories

### Story 6.0 — Coding-agent approach spike (blocks 6.3+)
**As** the builder, **I want** the code-generation mechanism decided from evidence, **so that** the
riskiest part of the product isn't built on an assumption.

**Acceptance criteria:**
- Options (custom tool-use loop vs. wrapping an existing engine) are evaluated against the
  document-Q&A MVP.
- A decision is recorded with rationale; the shape of Stories 6.3–6.5 follows from it.

### Story 6.1 — Development manager & task breakdown (FR-14)
**As** the builder, **I want** the MVP broken into an ordered task list, **so that** implementation
proceeds in a sensible sequence.

**Acceptance criteria:**
- Development Manager inspects the MVP spec and produces an ordered set of development tasks
  (Idea.MD §28, §30).

### Story 6.2 — Repository inspection (FR-15)
**As** the builder, **I want** agents to understand existing code before writing more, **so that**
they avoid unnecessary rewrites and follow conventions.

**Acceptance criteria:**
- A repository-inspection step runs before code is written (Idea.MD §31 Rule 1).

### Story 6.3 — Coding agents implement the MVP (FR-15)
**As** a consultant, **I want** the designed MVP implemented with tests, **so that** there's real
working code to demo.

**Acceptance criteria:**
- Frontend / Backend / AI Engineer agent roles implement the MVP and write accompanying tests
  (exact shape per the Story 6.0 decision).
- Working code is generated for the document-Q&A sample MVP.

### Story 6.4 — GitHub integration (FR-15)
**As** a consultant, **I want** a pull request opened for the generated code, **so that** I review
before anything merges.

**Acceptance criteria:**
- Branch + PR are created (Idea.MD §27, §32).
- Nothing is auto-merged or auto-deployed.

### Story 6.5 — Isolated execution (NFR5)
**As** the builder, **I want** generated code to run only in an isolated environment, **so that**
untrusted code never touches the main app process.

**Acceptance criteria:**
- Generated code executes only in an isolated environment, never directly in a production/shared
  process (Idea.MD §72, NFR5).

### Story 6.6 — Infra: vector DB & object storage
**As** the builder, **I want** Qdrant and MinIO available, **so that** the generated MVP has
retrieval and document storage.

**Acceptance criteria:**
- `qdrant` and `minio` services added to `docker-compose.yml`.
- `CODE_GENERATION` job type wired into the worker.

## Epic Definition of Done

- Working code is generated for the document-Q&A sample MVP; a GitHub PR is opened.
- Generated code only ever executes in the isolated environment.
- Tests pass (generated + our own); standing rules honored (see [index.md](index.md)).
