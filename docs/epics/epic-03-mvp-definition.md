---
epic: 3
title: MVP Definition
phase: 3
status: In Progress
depends_on: [2]
fr_covered: [FR-8, FR-9]
nfr_covered: [NFR7]
sources:
  - Idea.MD §18, §19, §20, §21, §23, §51
  - docs/plan.md Phase 3
  - PRD §5.3
---

# Epic 3 — MVP Definition

## Goal

From Meeting Intelligence, produce a deliberately small `MVPSpecification` — the smallest useful
product that could be demoed — not a full enterprise PRD. Every feature is classified, and
non-essential features are actively excluded rather than swept in.

## Dependencies

Epic 2 (Meeting Intelligence).

## Key decisions (this epic)

- Output size is a design constraint on the AI's proposal, not merely a UI limit: "small enough to
  demo," not "complete enough to build the full product" (NFR7).
- `MVPSpecification` is the central data contract for everything downstream (Idea.MD §19).

## Stories

### Story 3.1 — MVP specification schema (FR-8)
**As** the builder, **I want** a structured MVP spec schema, **so that** every later phase consumes
one stable contract.

**Acceptance criteria:**
- `MVPSpecification` schema per Idea.MD §19 (objective, target users, journeys, features, UI
  requirements, constraints, acceptance criteria, out-of-scope, assumptions, open questions, demo
  scenario, requirement traceability).
- Scope classification enum: `MUST_HAVE` / `SHOULD_HAVE` / `NICE_TO_HAVE` / `OUT_OF_SCOPE`
  (Idea.MD §21).

### Story 3.2 — MVP agent team (FR-8, NFR7)
**As** a consultant, **I want** a team of agents to propose then challenge the scope, **so that**
the result is genuinely minimal and demoable.

**Acceptance criteria:**
- Agent nodes: Product Manager, Feature Analyst, UX Analyst, Scope Analyst, Critic, Synthesizer
  (Idea.MD §18, §51).
- The Critic/Scope Analyst actively identifies and excludes non-essential features (FR-8
  consequence).
- Generated MVP stays small for the document-Q&A scenario (matches the spirit of Idea.MD §20/§71).

### Story 3.3 — MVP versioning (FR-9)
**As** a consultant, **I want** MVP specs versioned immutably once approved, **so that** approved
scope is never silently overwritten.

**Acceptance criteria:**
- Each MVP Specification is versioned.
- An already-approved version is never overwritten (Idea.MD §23).

### Story 3.4 — MVP job & API
**As** the builder, **I want** MVP generation to run as a job and be retrievable, **so that** the
frontend can display and manage it.

**Acceptance criteria:**
- `MVP_ANALYSIS` job type wired into the worker.
- `GET/POST /api/v1/projects/{id}/mvp` exist and are documented.

### Story 3.5 — MVP page (FR-20 partial)
**As** a consultant, **I want** to view the proposed MVP, **so that** I can assess it before
approving.

**Acceptance criteria:**
- MVP page shows objective, target users, journey, features by scope bucket, assumptions, open
  questions, acceptance criteria, demo scenario (Idea.MD §42). *(Approve/edit actions land in
  Epic 4.)*

### Story 3.6 — Scope-discipline evaluation (NFR7, SM-C1)
**As** the builder, **I want** to confirm the MVP stays small across fixtures, **so that** "more
proposed" is never mistaken for success.

**Acceptance criteria:**
- Running all 5 mock transcripts yields a small MVP each time (sanity-checked against SM-C1).

## Epic Definition of Done

- For the document-Q&A mock scenario, the generated MVP matches the spirit of Idea.MD §20/§71
  (small, demoable, not the full feature list).
- Every feature carries a scope classification; non-essentials are marked `OUT_OF_SCOPE`.
- Tests pass; standing rules honored (see [index.md](index.md)).
