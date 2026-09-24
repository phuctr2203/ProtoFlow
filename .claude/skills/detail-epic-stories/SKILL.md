---
name: detail-epic-stories
description: 'Flesh out the stories of a ProtoFlow epic with detailed acceptance criteria and a task checklist. Use when the user says "detail epic N", "detail the stories for epic N", or "/detail-epic-stories N".'
---

# Detail Epic Stories

**Goal:** Take one existing epic file under `docs/epics/` and enrich **each story it already
contains** with (a) clear, testable **Acceptance Criteria** and (b) a **Tasks** checklist the
developer can tick off. Do this without inventing new scope.

**Your role:** a delivery lead turning an epic's story list into something a single developer can
pick up and execute. You bring implementation detail; you do not redesign the plan.

## Inputs

Argument: an epic number (`0`–`9`) or an epic file path. Resolve the epic file as
`docs/epics/epic-0<N>-*.md` when given a number.

Read, in this order, for grounding:
1. The target epic file itself (its stories, goal, `fr_covered`, and `sources` frontmatter).
2. `docs/plan.md` — the matching `## Phase <N>` section (task lists + Definition of Done).
3. `Idea.MD` — the specific `§` sections named in the epic's frontmatter `sources` and stories.
4. `_bmad-output/planning-artifacts/prds/prd-IdeaForge-2026-09-17/prd.md` — the FR text for each
   `FR-n` the epic covers.
5. `docs/epics/index.md` — the shared Definition of Done and Standing rules.

## Hard rules (do not break)

- 🔒 **Keep the existing stories as they are** — same numbering, same titles, same
  `As a / I want / so that` line. Do **not** reorder, renumber, split, merge, add, or delete
  stories. If a story looks wrong, say so to the user and stop — do not silently change it.
- ➕ Only **add** two subsections to each story: `**Acceptance criteria:**` and `**Tasks:**`.
  If they already exist, refresh them in place.
- 🎯 Every acceptance criterion must be **testable** (a reviewer can objectively say pass/fail).
  Cite the source in parentheses where it helps: `(FR-5)`, `(Idea.MD §17)`, `(NFR3)`.
- ✅ Tasks are concrete implementation steps written as a GitHub checklist (`- [ ]`), ordered so a
  developer can do them top to bottom. Tasks describe *work to do*; acceptance criteria describe
  *what must be true when done* — keep the two distinct.
- 🧱 Create only the tables/entities/services a story actually needs — never "set up everything" in
  one story (mirrors the domain-first, incremental principle in Idea.MD §81/§83).
- 🚫 Do not touch the epic's `## Goal`, `## Dependencies`, `## Key decisions`, or
  `## Epic Definition of Done` sections, except to leave them intact.
- Respect the project's Standing rules (see `docs/epics/index.md`): async jobs for long AI work,
  idempotent events, structured outputs, traceability, inferred ≠ confirmed, no out-of-scope creep.

## Output format (per story)

```
### Story <N>.<M> — <existing title>
**As a** <role>, **I want** <capability>, **so that** <value>.

**Acceptance criteria:**
- <testable outcome> (<source ref>)
- <testable outcome incl. an error / edge case>

**Tasks:**
- [ ] <concrete step>
- [ ] <concrete step>
- [ ] Tests: <what to test> (unit/integration as fits)
```

Include at least one **error / edge-case** acceptance criterion per story where one is plausible
(e.g. duplicate input, validation failure, retry) and a **Tests** task on every story (the DoD
requires tests).

## Procedure

1. Resolve and read the epic file; list its current stories back to the user so they can confirm
   the set is right before you expand it.
2. Read the grounding inputs above for that phase.
3. For each existing story, draft `Acceptance criteria` + `Tasks` per the format.
4. Rewrite the epic file's `## Stories` section in place, replacing each story with its enriched
   version. Leave every other section untouched.
5. Add `storiesDetailed: true` to the epic file's frontmatter.
6. Report a short summary: how many stories were detailed, and any story you flagged as unclear.

## Notes

- This skill enriches an epic that already has a story list (created earlier by hand or by
  `bmad-create-epics-and-stories`). It is deliberately lighter than that skill — no new epics, no
  requirements extraction, no multi-step gate.
- To run it for another epic later: `/detail-epic-stories <N>` (e.g. `/detail-epic-stories 1`).
