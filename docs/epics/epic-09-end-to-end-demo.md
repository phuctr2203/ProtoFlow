---
epic: 9
title: End-to-End Demo
phase: 9
status: Not Started
depends_on: [8]
fr_covered: [FR-20]
validates: [SM-1]
sources:
  - Idea.MD §38, §39, §70, §85
  - docs/plan.md Phase 9
  - PRD §5.9, §10 (SM-1)
---

# Epic 9 — End-to-End Demo

## Goal

The full success scenario runs start to finish without manual data-fixing: create project →
simulated meeting → transcript → intelligence → MVP proposal → human approval → design → generated
code (PR) → QA → working MVP → demo package. This epic also completes the cross-phase Project
Workspace view (FR-20).

## Dependencies

Epic 8 (Demo Preparation) — and, transitively, every prior epic.

## Stories

### Story 9.1 — Project workspace status view (FR-20)
**As** a consultant, **I want** one place showing where an engagement stands across all phases, **so
that** I can see status at a glance.

**Acceptance criteria:**
- Project overview shows current stage and status of Meeting, MVP, Design, Development, QA, and Demo
  (Idea.MD §38, §39).
- Each phase's status reflects the real state produced by Epics 1–8.

### Story 9.2 — Full end-to-end walkthrough (SM-1)
**As** the builder, **I want** to run the whole pipeline on one simulated meeting, **so that** I can
prove the core promise.

**Acceptance criteria:**
- A single simulated client meeting flows through the entire pipeline (Idea.MD §70, §85) without
  manual data-fixing along the way (validates SM-1 / FR-1…FR-19).

### Story 9.3 — Close integration gaps
**As** the builder, **I want** any seams found during the walkthrough fixed, **so that** the flow is
reliable, not one-off.

**Acceptance criteria:**
- Integration gaps found in Story 9.2 are fixed and the walkthrough re-runs cleanly.

### Story 9.4 — Document the working demo
**As** the builder, **I want** the working demo documented, **so that** it can be reproduced and
shown.

**Acceptance criteria:**
- The end-to-end demo is documented (how to run it, expected output).

## Epic Definition of Done

- The full success scenario completes without manual data-fixing along the way (Idea.MD §85, SM-1).
- The Project workspace reflects real cross-phase status (FR-20).
- Standing rules honored (see [index.md](index.md)).
