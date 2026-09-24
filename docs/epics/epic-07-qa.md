---
epic: 7
title: Automated QA
phase: 7
status: Not Started
depends_on: [6]
fr_covered: [FR-16, FR-17]
sources:
  - Idea.MD §33, §34, §45
  - docs/plan.md Phase 7
  - PRD §5.7
---

# Epic 7 — Automated QA

## Goal

Before anything is demoed, validate the implemented MVP against its original requirements and
acceptance criteria — not just "does it run" — and report requirement coverage. Every `MUST_HAVE`
requirement must have at least one mapped test before a Project can be marked demo-ready.

## Dependencies

Epic 6 (AI-Assisted Development).

## Stories

### Story 7.1 — Test generation (FR-16)
**As** a consultant, **I want** test cases generated from requirements and acceptance criteria,
**so that** validation traces back to what the client asked for.

**Acceptance criteria:**
- QA Agent generates test cases from the MVP's requirements and acceptance criteria (Idea.MD §33).

### Story 7.2 — Test execution & evidence (FR-16)
**As** a consultant, **I want** tests executed with recorded results, **so that** pass/fail is
evidence-backed.

**Acceptance criteria:**
- Tests are executed; each records PASS/FAIL with evidence and a failure reason where applicable
  (Idea.MD §33, §76).

### Story 7.3 — End-to-end traceability (FR-17)
**As** a consultant, **I want** a Requirement → Feature → Task → Code → Test chain, **so that**
coverage is auditable end to end.

**Acceptance criteria:**
- The traceability chain from requirement through to test is maintained (Idea.MD §34).

### Story 7.4 — Coverage reporting & job (FR-17)
**As** a consultant, **I want** a coverage rollup, **so that** I know whether the MVP is demo-ready.

**Acceptance criteria:**
- `QA` job type wired into the worker.
- The report shows, per requirement, whether it's covered by ≥1 test, rolled up into overall
  coverage and pass/fail counts.
- Every `MUST_HAVE` requirement has at least one mapped test before the Project can be marked
  demo-ready.

### Story 7.5 — QA page (FR-20 partial)
**As** a consultant, **I want** to view the QA report, **so that** I can judge readiness at a glance.

**Acceptance criteria:**
- QA page shows total/passed/failed/blocked and requirement + acceptance-criteria coverage
  (Idea.MD §45).

## Epic Definition of Done

- QA report shows requirement coverage % and pass/fail counts.
- Every `MUST_HAVE` requirement has at least one mapped test.
- Tests pass; standing rules honored (see [index.md](index.md)).
