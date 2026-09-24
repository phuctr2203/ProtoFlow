# Working with BMAD in ProtoFlow

A practical guide to how this repo uses **BMAD** (Breakthrough Method for Agile AI-Driven
development) to go from idea → PRD → epics/stories → working code. It's tailored to *this* project's
actual setup and current state — not the generic BMAD docs.

- **Module:** `bmm` (BMAD Method) · **Version:** 6.12.0
- **Config:** [`_bmad/bmm/config.yaml`](../_bmad/bmm/config.yaml) — user `Trhp`, language English
- **Source spec:** [`Idea.MD`](../Idea.MD) (90-section technical spec) · **Hand plan:**
  [`docs/plan.md`](plan.md)

---

## 1. How to run a BMAD skill

BMAD ships as **skills** (a.k.a. slash commands / agents). In this desktop app you invoke one three
ways — all equivalent:

- Type the slash command: `/bmad-prd`, `/bmad-create-epics-and-stories`, …
- Ask by name: *"create the epics and stories list"*, *"run sprint planning"*.
- Talk to a **persona**: *"talk to Amelia"*, *"I want the architect"*.

Skills live under [`.claude/skills/`](../.claude/skills/) (rendered from `_bmad/`). You don't run the
files directly — you invoke the skill and it drives an interactive workflow with you.

### The personas (agents)

| Persona | Role | Skill | Use for |
|---|---|---|---|
| **Mary** | Business Analyst | `bmad-agent-analyst` | market/competitive research, requirements |
| **John** | Product Manager | `bmad-agent-pm` | PRD creation, requirements discovery |
| **Winston** | Architect | `bmad-agent-architect` | system/technical design |
| **Sally** | UX Designer | `bmad-agent-ux-designer` | UX/UI design |
| **Amelia** | Developer | `bmad-agent-dev` | implementing stories / code changes |

---

## 2. The workflow pipeline

BMAD splits into **Plan** (decide what to build) and **Ship** (build and verify it).

```text
PLAN
  bmad-product-brief / bmad-forge-idea      → shape the idea
  bmad-prd                                  → PRD (what & why)
  bmad-architecture                         → Architecture (how, cross-cutting)
  bmad-ux                                    → DESIGN.md + EXPERIENCE.md (if UI)
  bmad-create-epics-and-stories             → epics + stories
  bmad-sprint-planning                      → readiness check + sprint status tracker
        │
        ▼
SHIP  (per story, in order)
  bmad-agent-dev (Amelia) / bmad-build      → implement a story → code
  bmad-code-review                          → parallel reviewers → triaged findings
  bmad-qa-generate-e2e-tests                → API/E2E tests for a feature
  bmad-walkthrough                          → guided human review of a change
  bmad-retrospective                        → review a finished epic, accept/close
```

Supporting skills, any time: `bmad-brainstorming`, `bmad-deep-recon` (research),
`bmad-advanced-elicitation` (deeper critique), `bmad-correct-course` (mid-sprint scope change),
`bmad-party-mode` (multi-persona roundtable), `bmad-help` (what should I do next?),
`bmad-customize` (override skill behavior).

---

## 3. Where artifacts live

Set in [`_bmad/bmm/config.yaml`](../_bmad/bmm/config.yaml):

| What | Location |
|---|---|
| Planning artifacts (PRD, epics, architecture, UX) | `_bmad-output/planning-artifacts/` |
| Implementation artifacts | `_bmad-output/implementation-artifacts/` |
| Project knowledge (curated docs) | `docs/` |
| BMAD engine + skills | `_bmad/`, `.claude/skills/` |
| Customization overrides | `_bmad/custom/*.toml` |

---

## 4. Where ProtoFlow is right now

| Stage | Status | Where |
|---|---|---|
| Idea / spec | ✅ Done | [`Idea.MD`](../Idea.MD) |
| Product brief / discovery | ✅ Folded into the PRD | — |
| **PRD** | ✅ Done | [`prd.md`](../_bmad-output/planning-artifacts/prds/prd-IdeaForge-2026-09-17/prd.md) + [`addendum.md`](../_bmad-output/planning-artifacts/prds/prd-IdeaForge-2026-09-17/addendum.md) |
| Architecture.md | ⚠️ Not written — `addendum.md` + `Idea.MD` stand in | — |
| UX contract (DESIGN/EXPERIENCE) | ⚠️ None | — |
| **Epics + story list** | ✅ Done | [`docs/epics/`](epics/) — [`index.md`](epics/index.md) + `epic-00…09` |
| **Story detail (AC + tasks)** | 🔄 Epic 0 done; Epics 1–9 pending | [`epic-00-foundation.md`](epics/epic-00-foundation.md) |
| Sprint planning | ⬜ Not started | — |
| Implementation | ⬜ Not started | — |

Each phase in [`docs/plan.md`](plan.md) maps to one epic (**Epic N ↔ Phase N**). The FR→epic
coverage map and epic list are in [`docs/epics/index.md`](epics/index.md).

> **Note:** the PRD/epics supersede `docs/plan.md` as the source of truth going forward (see the
> addendum); treat `plan.md` as the original hand-written reference.

---

## 5. The typical loop for one epic

1. **Detail the stories** — add acceptance criteria + task checklists:
   ```bash
   /detail-epic-stories 1
   ```
   This is a **custom skill** for this repo (see §6). Do this before implementing.
2. **(Optional) Sprint planning** — generate/refresh the sprint tracker: *"run sprint planning"*.
3. **Implement, story by story, in order** — *"talk to Amelia"* or `/bmad-build`, one story at a
   time. Don't start a story that depends on a later one.
4. **Review & test** — `/bmad-code-review`, `/bmad-qa-generate-e2e-tests`.
5. **Close the epic** — `/bmad-retrospective`, then flip the epic's `status:` and the row in
   [`index.md`](epics/index.md) to `Done`.

**Work epics in dependency order (0 → 9).** Don't start an epic until the previous epic's Definition
of Done is met (incremental pipeline — Idea.MD §83/§88).

---

## 6. Custom skill: `detail-epic-stories`

A repo-specific skill ([`.claude/skills/detail-epic-stories/SKILL.md`](../.claude/skills/detail-epic-stories/SKILL.md))
that enriches an epic's **existing** stories with detailed **acceptance criteria** + a **task
checklist**, grounded in `plan.md` / `Idea.MD` / the PRD.

```bash
/detail-epic-stories <N>      # N = 0..9, e.g. /detail-epic-stories 2
```

- Keeps the story set exactly as-is — no reorder, renumber, add, or drop.
- Adds `Acceptance criteria` (testable, with `(FR-x)` / `(Idea.MD §y)` refs + an edge case) and a
  `Tasks:` checklist (`- [ ]`) with a Tests task per story.
- Leaves Goal / Dependencies / Decisions / DoD untouched; sets `storiesDetailed: true`.

It's deliberately lighter than `bmad-create-epics-and-stories` (which *creates* epics and does full
requirements extraction). Use `detail-epic-stories` when the epic already has a story list and you
just want it implementation-ready.

---

## 7. Conventions & guardrails

Apply to every epic (from Idea.MD §79/§88, mirrored in [`index.md`](epics/index.md)):

**Definition of Done (per feature):** implementation + tests + error handling + logs + documented
API + usable UI + DB migration (if needed) + no secrets committed + acceptance criteria satisfied.

**Standing rules (every epic):**
- No out-of-scope creep (pricing, estimation, resourcing, full PM, k8s — PRD §6).
- Inferred requirements are never presented as confirmed.
- Requirement traceability is maintained.
- All AI-critical data uses structured (Pydantic) outputs.
- Long-running AI work stays in async jobs — never inline in a request/webhook.
- Webhook/event processing stays idempotent.

---

## 8. Customizing BMAD

To change a skill's behavior without editing the skill itself, add overrides under
`_bmad/custom/` (base → team `<skill>.toml` → personal `<skill>.user.toml`), or run
`/bmad-customize`. Config values (name, language, output paths) live in
[`_bmad/bmm/config.yaml`](../_bmad/bmm/config.yaml).

---

## 9. Quick reference

```text
Plan
  /bmad-prd                          create/update/validate the PRD
  /bmad-architecture                 create the architecture spine
  /bmad-ux                           DESIGN.md + EXPERIENCE.md
  /bmad-create-epics-and-stories     epics + story list
  /detail-epic-stories N             ← this repo: AC + tasks for epic N
  /bmad-sprint-planning              readiness check + sprint status

Ship
  talk to Amelia  /  /bmad-build     implement a story
  /bmad-code-review                  review a diff/PR
  /bmad-qa-generate-e2e-tests        generate API/E2E tests
  /bmad-walkthrough                  guided human review
  /bmad-retrospective                close out an epic

Anytime
  /bmad-help                         what should I do next?
  /bmad-brainstorming  /bmad-deep-recon  /bmad-correct-course
```
