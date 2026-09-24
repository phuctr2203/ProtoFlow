---
epic: 4
title: Human Approval
phase: 4
status: In Progress
depends_on: [3]
fr_covered: [FR-10, FR-11]
sources:
  - Idea.MD §22, §75
  - docs/plan.md Phase 4
  - PRD §5.4
---

# Epic 4 — Human Approval

## Goal

An MVP definition cannot silently proceed to Design or Development. A human must Approve, Reject,
Edit, or Request Revision on an MVP version, and downstream phases are hard-blocked until an
approved version exists.

## Dependencies

Epic 3 (MVP Definition).

## Key decisions (this epic)

- The approval gate is a hard guard, not a UI convention — attempting to start Design without an
  approved MVP is refused server-side (FR-11, Idea.MD §75).

## Stories

### Story 4.1 — Approval record (FR-10)
**As** the builder, **I want** approvals persisted, **so that** every scope decision is auditable.

**Acceptance criteria:**
- `MVPApproval` model + migration capturing project, version, approved_by, approved_at, comments
  (Idea.MD §22).

### Story 4.2 — Approval decision endpoint (FR-10)
**As** a consultant, **I want** to act on a proposed MVP version, **so that** I control what gets
built.

**Acceptance criteria:**
- `POST /api/v1/projects/{id}/mvp/approve` supports Approve / Reject / Request Revision, persisting
  who / when / comments.
- Editing an MVP produces a new version rather than mutating an approved one (ties to Story 3.3).

### Story 4.3 — Downstream guard (FR-11)
**As** the builder, **I want** Design/Development blocked without approval, **so that** the AI never
runs ahead of human judgment.

**Acceptance criteria:**
- Starting Design or Development without an approved MVP version is refused, not silently allowed.

### Story 4.4 — Approval UI (FR-10)
**As** a consultant, **I want** approval actions on the MVP page, **so that** I can decide in one
place.

**Acceptance criteria:**
- MVP page exposes Approve / Reject / Edit / Request Revision actions (Idea.MD §42).
- The current approval state and version are visible.

## Epic Definition of Done

- Starting Design without an approved MVP is blocked.
- Approval is persisted with version, approver, timestamp, comments.
- Tests pass; standing rules honored (see [index.md](index.md)).
