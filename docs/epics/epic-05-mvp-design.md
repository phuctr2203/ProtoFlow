---
epic: 5
title: MVP Design
phase: 5
status: In Progress
depends_on: [4]
fr_covered: [FR-12, FR-13]
sources:
  - Idea.MD §24, §25, §26, §43
  - docs/plan.md Phase 5
  - PRD §5.5
---

# Epic 5 — MVP Design

## Goal

From an approved MVP, generate just enough UX flow and technical design to guide implementation —
target 1–5 pages equivalent, not a heavyweight architecture document — with no manual intervention
once an MVP is approved.

## Dependencies

Epic 4 (Human Approval) — design consumes an *approved* MVP version.

## Stories

### Story 5.1 — UX design agent (FR-12)
**As** a consultant, **I want** the MVP's UX flow and screens generated, **so that** implementation
has a clear interaction map.

**Acceptance criteria:**
- UX Agent generates user journey, screen list, navigation, and key UI states (Idea.MD §25).

### Story 5.2 — Solution design agent (FR-13)
**As** a consultant, **I want** a lightweight technical design generated, **so that** development
agents have architecture guidance without over-engineering.

**Acceptance criteria:**
- Solution Design Agent produces components, APIs, data model, AI workflow, integrations, and key
  technology decisions (Idea.MD §26).
- Output is scaled to roughly 1–5 pages equivalent (not a huge architecture document).

### Story 5.3 — Design job & API
**As** the builder, **I want** design generation to run as a job and be retrievable, **so that**
the frontend can render it.

**Acceptance criteria:**
- `MVP_DESIGN` job type wired into the worker.
- `GET /api/v1/projects/{id}/design` exists and is documented.
- Design generation requires no manual intervention once an MVP is approved (FR-13 consequence).

### Story 5.4 — Design page (FR-20 partial)
**As** a consultant, **I want** to view the generated design, **so that** I can review it before
development.

**Acceptance criteria:**
- Design page shows user journey, screens, architecture, components, APIs, data model, and technical
  decisions (Idea.MD §43).

## Epic Definition of Done

- Design generates from an approved MVP without manual intervention.
- Output stays lightweight (1–5 pages equivalent).
- Tests pass; standing rules honored (see [index.md](index.md)).
