---
epic: 8
title: Demo Preparation
phase: 8
status: Not Started
depends_on: [7]
fr_covered: [FR-18, FR-19]
sources:
  - Idea.MD §35, §36, §37, §46
  - docs/plan.md Phase 8
  - PRD §5.8
---

# Epic 8 — Demo Preparation

## Goal

Package the validated MVP into something a consultant can run live for a client, without
overclaiming. Every capability shown is labeled `IMPLEMENTED`, `SIMULATED`, or `NOT_IMPLEMENTED`,
and the demo script and package never present simulated functionality as production functionality.

## Dependencies

Epic 7 (Automated QA).

## Stories

### Story 8.1 — Demo agent (FR-18)
**As** a consultant, **I want** a demo objective and script generated, **so that** I can run a
confident, structured demo.

**Acceptance criteria:**
- Demo Agent generates a demo objective and a step-by-step demo script (Idea.MD §35).

### Story 8.2 — Synthetic demo data (FR-18)
**As** a consultant, **I want** realistic sample data generated, **so that** the demo shows the
product working on plausible inputs.

**Acceptance criteria:**
- Sample documents/users/questions/records are generated and clearly marked as synthetic
  (Idea.MD §36).

### Story 8.3 — Honest status labeling (FR-19)
**As** a consultant, **I want** every capability honestly labeled, **so that** I never overpromise
to a client.

**Acceptance criteria:**
- Every capability is labeled `IMPLEMENTED` / `SIMULATED` / `NOT_IMPLEMENTED` (Idea.MD §37).
- The demo script and demo package agree on labels — nothing scripted as real when marked
  `SIMULATED` (FR-19 consequence).

### Story 8.4 — Demo job, API & page (FR-20 partial)
**As** a consultant, **I want** the demo package viewable with a launch action, **so that** I can
run it from the workspace.

**Acceptance criteria:**
- `DEMO_PREPARATION` job type wired into the worker.
- `GET /api/v1/projects/{id}/demo` exists and is documented.
- Demo page shows objective, script, data, implemented/simulated/known limitations/next steps, with
  a Start Demo action (Idea.MD §46).

## Epic Definition of Done

- Demo package includes an honest `IMPLEMENTED` / `SIMULATED` / `NOT_IMPLEMENTED` breakdown.
- Demo script matches what was actually built (no overclaiming, Idea.MD §37).
- Tests pass; standing rules honored (see [index.md](index.md)).
