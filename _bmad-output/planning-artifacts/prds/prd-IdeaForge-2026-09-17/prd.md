---
title: ProtoFlow
status: draft
created: 2026-09-17
updated: 2026-09-17
---

# PRD: ProtoFlow
*Working title — confirm.*

## 0. Document Purpose
This PRD defines what ProtoFlow is and why, for the solo builder (Trhp) acting as PM/architect/dev, and for the downstream BMAD workflows (`bmad-architecture`, `bmad-create-epics-and-stories`) that consume it next. Vocabulary is Glossary-anchored (§3); each Feature (§5) groups its Functional Requirements (FR-N, numbered globally) beneath it; assumptions made without explicit confirmation are tagged inline `[ASSUMPTION]` and indexed in §12. This PRD consolidates the full technical spec already written in `Idea.MD` and the architecture/stack decisions made in prior discussion — it defines *what* and *why*; the *how* (tech stack, service sequencing, mock-fixture design) lives in `addendum.md` and `Idea.MD` for the architecture phase to consume.

## 1. Vision
ProtoFlow turns a client discovery meeting into a working, demoable MVP, compressing a process that normally takes days or weeks of BA analysis, PRD writing, and design before a client sees anything tangible. After a meeting, ProtoFlow automatically ingests the transcript, extracts structured "meeting intelligence" (requirements, personas, constraints, decisions, risks) with every important extraction traceable back to the exact transcript moment that supports it, and proposes the smallest useful MVP that could be demonstrated — not a full enterprise product. A human reviews and approves that MVP before anything else happens; once approved, ProtoFlow generates a lightweight design, has AI development agents implement it against a real Git repository, runs automated QA against the original requirements, and packages an honest demo that clearly separates what's actually working from what's simulated.

The core question the product answers is: *"After talking to this client, what is the smallest useful product we can build and demonstrate?"* — and the core promise is that a client can talk to you in the morning and, by the end of the workflow, you have something tangible to show them.

## 2. Why Now
Meeting-intelligence tools (Fathom, Fireflies, Otter) stop at summaries and action items. Requirement-extraction tools exist but stop at a documented list. AI prototype generators (v0, Bolt, Lovable, Replit Agent) produce working code fast, but only from a human-written prompt — they assume discovery already happened. No product found chains a raw client conversation all the way through to working, QA'd, honestly-labeled code with a human approval gate and evidence traceability intact — the market splits into tools that stop at documentation and tools that stop at code. The pieces this needs (capable LLMs for structured extraction, agentic coding tools, cheap async compute) are newly practical together; consulting discovery is still done by hand.

## 3. Target User
[ASSUMPTION: ProtoFlow v1 has exactly one type of user — an independent software consultant (the builder) running real client discovery calls. There is no multi-seat/team account model in v1, and the end client never logs into ProtoFlow directly — they only see the demo output.]

### 3.1 Jobs To Be Done
- As an independent consultant, I want the days between a client meeting and a demoable prototype compressed to same-day/next-day, so the client stays engaged and I can validate direction before investing in a full build.
- As an independent consultant, I want every requirement I show a client traced back to something they actually said, so I never present my own assumptions as their confirmed scope.
- As an independent consultant, I want to control what actually gets built (approve/reject/edit) before any code is written, so the AI never runs ahead of my judgment on scope.
- As an independent consultant, I want a demo I can trust — one that's honest about what's real vs. simulated — so I don't overpromise to a client and damage trust.

### 3.2 Non-Users (v1)
- Other consultants/teams using ProtoFlow as a shared multi-tenant product — v1 is single-operator. [ASSUMPTION]
- The end client as a direct ProtoFlow user — they attend the meeting and view the demo, but never log into the app itself.
- Enterprises wanting full project delivery (estimation, pricing, resourcing, production deployment) — explicitly out of scope (§6).

### 3.3 Key User Journeys

**UJ-1. Mai runs a discovery call and has a demo ready before the follow-up.**
- **Persona + context:** Mai is an independent software consultant. A prospective client has just described wanting "an AI system so employees can ask questions about our internal documents" — vague, no written requirements.
- **Entry state:** Mai is logged into ProtoFlow, has created a Project for this prospect, and starts a meeting from the Project workspace.
- **Path:** Mai and the client talk normally for 30-45 minutes; the client mentions their documents are mostly PDF, some in Vietnamese, and that employees waste time searching for information. The meeting ends. ProtoFlow automatically receives the transcript, processes it in the background, and Mai gets a notification that Meeting Intelligence is ready. She opens the Intelligence page and reviews extracted requirements, each with a quote and timestamp from the actual conversation. ProtoFlow proposes a small MVP: upload documents, ask questions in natural language, get an answer with source citations — explicitly leaving out SSO, admin tooling, and analytics as out-of-scope. Mai edits one requirement's priority, then approves the MVP.
- **Climax:** ProtoFlow generates a lightweight design and opens a GitHub PR implementing the MVP; Mai reviews the QA report (all MUST_HAVE requirements covered, tests passing) and opens the Demo page, which shows a ready-to-run demo script and clearly marks authentication as `SIMULATED`.
- **Resolution:** Mai runs the demo live on her next call with the client — upload a sample document, ask a real question, get a sourced answer — and the client can now see and react to something concrete instead of a slide deck.
- **Edge case:** if the transcript is noisy (client spoke quickly, or the recording captured cross-talk) and confidence on a requirement is low, that requirement shows as `NEEDS_REVIEW` instead of being silently included in the MVP, and Mai resolves it manually before approving.

## 4. Glossary
- **Meeting** — A single client conversation tied to a Project, with a lifecycle from scheduled through transcript-ready to processed.
- **Transcript** — The raw and normalized text of a Meeting's conversation, broken into speaker-attributed segments.
- **Meeting Intelligence** — The structured output of processing a Transcript: business context, requirements, personas, constraints, decisions, risks, open questions, and action items.
- **Requirement** — A single functional or non-functional need, marked `EXPLICIT` (directly stated by the client) or `INFERRED` (derived by ProtoFlow, never presented as client-confirmed), carrying a priority, status, and confidence score.
- **Evidence** — The specific transcript quote, speaker, and timestamp that supports a Requirement (or other extracted item). A Requirement without supporting Evidence is marked `NEEDS_REVIEW` rather than treated as confirmed.
- **MVP Specification** — The single small, versioned definition of "what we will build to demo," derived from Meeting Intelligence: objective, target users, user journeys, features (classified `MUST_HAVE`/`SHOULD_HAVE`/`NICE_TO_HAVE`/`OUT_OF_SCOPE`), acceptance criteria, out-of-scope items, assumptions, and a demo scenario.
- **Human Approval Gate** — The mandatory checkpoint where a human must Approve, Reject, Edit, or Request Revision on an MVP Specification version before Design or Development can begin.
- **MVP Design** — The lightweight UX flow and technical design generated from an approved MVP Specification.
- **Development Task** — A unit of implementation work broken down from the MVP Specification and assigned to a development agent role.
- **QA Report** — The result of validating the implemented MVP against its Requirements and Acceptance Criteria: pass/fail per test, with requirement coverage.
- **Demo Package** — The client-facing deliverable: demo objective, script, sample data, and an explicit `IMPLEMENTED` / `SIMULATED` / `NOT_IMPLEMENTED` breakdown of every capability shown.
- **Project** — The top-level container for one client engagement, holding its Meetings, Intelligence, MVP versions, Design, Development, QA, and Demo state.

## 5. Features

### 5.1 Meeting Capture & Transcript Ingestion
**Description:** ProtoFlow receives notice that a meeting's transcript is ready, retrieves it, and makes it available for processing — without ever running long AI work inline in that notification path. In v1, meetings are simulated through a mock provider rather than a live video platform, so the full pipeline can be exercised and evaluated without depending on a real meeting service. [ASSUMPTION: "meeting provider" is pluggable by design so a real provider can be added later without touching downstream logic — mechanism detail in `addendum.md`.]

**Functional Requirements:**

#### FR-1: Receive meeting-completion notification
The system can receive a "transcript ready" notification for a Meeting and acknowledge it in under 2 seconds, deferring all processing to the background.
**Consequences (testable):**
- Notification handling never blocks on an LLM call or any long-running work.
- The same notification delivered twice does not result in duplicate processing.

#### FR-2: Retrieve and normalize a transcript
The system can retrieve a Meeting's raw transcript and normalize it into speaker-attributed segments with timestamps.
**Consequences (testable):**
- Each segment has a speaker, start time, end time, and text.
- Processing failures are retried and expose an error reason rather than failing silently.

#### FR-3: Simulate meetings for development and evaluation
A consultant (or the system in test mode) can trigger a simulated meeting-completion event using a pre-built transcript, covering a range of realistic transcript quality — clean, fast/unclear speech, ambiguous speaker attribution, and mixed-language content.
**Consequences (testable):**
- At least 5 distinct simulated transcripts are available, each representing a different realistic quality/noise profile.
- Every simulated transcript flows through the full pipeline without manual intervention.

**Out of Scope:** Real integration with a live meeting/video platform. [see §7.2]

### 5.2 Meeting Intelligence Extraction
**Description:** ProtoFlow reads a normalized transcript and produces structured project knowledge: who the client is, what problem they have, what they want, who will use it, what's required, what's constrained, what was decided, what's still open, and what risks exist. Every important item is either backed by Evidence from the transcript or explicitly marked as ProtoFlow's own inference — never blended together silently. Realizes UJ-1.

**Functional Requirements:**

#### FR-4: Extract business context, problem, and goals
The system can extract the client's business context, the problem they described, and their desired outcomes from a transcript.
**Consequences (testable):**
- Output distinguishes stated business impact from ProtoFlow's own interpretation.

#### FR-5: Extract requirements with evidence
The system can extract functional and non-functional requirements, each carrying an `EXPLICIT`/`INFERRED` marking, a priority, and either supporting Evidence (quote, speaker, timestamp) or a `NEEDS_REVIEW` status.
**Consequences (testable):**
- No requirement is presented as `EXPLICIT`/confirmed without a supporting quote and timestamp.
- Requirements extracted from a noisy or ambiguous transcript segment receive lower confidence or `NEEDS_REVIEW`, not false confidence.

#### FR-6: Extract personas, constraints, decisions, risks, open questions, and action items
The system can extract user personas/roles, technical/regulatory constraints, decisions explicitly made in the meeting, risks, unresolved open questions, and action items (with owner/deadline where mentioned).

#### FR-7: Validate extracted evidence
The system can check, for every important extracted item, that Evidence exists, actually supports the claim, has a correctly attributed speaker and a timestamp, and that inferred items are marked as such — flagging weak evidence as `NEEDS_REVIEW` instead of dropping or silently accepting it.
**Consequences (testable):**
- A requirement whose evidence doesn't actually support its description is flagged, not passed through.

**Feature-specific NFRs:**
- Confidence thresholds (what counts as high/medium/needs-review) are configurable, not hardcoded.

### 5.3 MVP Definition
**Description:** From Meeting Intelligence, ProtoFlow proposes the smallest useful product that could be demonstrated — deliberately resisting the urge to propose a full-featured system. Realizes UJ-1.

**Functional Requirements:**

#### FR-8: Propose a scoped MVP
The system can generate an MVP Specification — objective, target users, core user journey, candidate features, acceptance criteria, and a demo scenario — from Meeting Intelligence.
**Consequences (testable):**
- Every feature is classified `MUST_HAVE` / `SHOULD_HAVE` / `NICE_TO_HAVE` / `OUT_OF_SCOPE`.
- The proposal actively identifies and excludes non-essential features rather than including everything technically implied by the requirements.

#### FR-9: Version MVP specifications
The system can version each MVP Specification and never overwrites an already-approved version.

**Feature-specific NFRs:**
- Output size targets "small enough to demo," not "complete enough to build the full product" — this is a design constraint on the AI's proposal, not just a UI limit.

### 5.4 Human Approval Gate
**Description:** No MVP proceeds to Design or Development without an explicit human decision. Realizes UJ-1.

**Functional Requirements:**

#### FR-10: Approve, reject, edit, or request revision on an MVP version
A consultant can Approve, Reject, Edit, or Request Revision on a proposed MVP Specification version, with the decision (who, when, comments) persisted.

#### FR-11: Block downstream phases until approval
The system prevents Design and Development from starting on a Project until it has an approved MVP Specification version.
**Consequences (testable):**
- Attempting to start Design without an approved MVP is refused, not silently allowed.

### 5.5 MVP Design
**Description:** From an approved MVP, ProtoFlow produces just enough UX and technical design to guide implementation — not a heavyweight architecture document.

**Functional Requirements:**

#### FR-12: Generate UX flow and screen definitions
The system can generate the user journey, screen list, navigation, and key UI states for the approved MVP.

#### FR-13: Generate a lightweight technical design
The system can generate a technical design covering components, APIs, data model, AI workflow, and key technology decisions for the approved MVP, scaled to roughly 1-5 pages equivalent.
**Consequences (testable):**
- Design generation requires no manual intervention once an MVP is approved.

### 5.6 AI-Assisted Development
**Description:** ProtoFlow's development agents implement the designed MVP against a real Git repository, producing a reviewable pull request rather than deploying anything automatically.

**Functional Requirements:**

#### FR-14: Break the MVP into implementation tasks
The system can break an approved, designed MVP into an ordered set of development tasks.

#### FR-15: Implement the MVP against a real repository
Development agents can inspect the existing repository, implement the designed MVP, write accompanying tests, and open a pull request for human review — never merging or deploying autonomously.
**Consequences (testable):**
- Generated code executes only in an isolated environment, never directly in a production or shared process.
- A pull request is opened; nothing is auto-merged.

**Feature-specific NFRs:**
- Security: generated/untrusted code must never execute outside the isolated environment.

**Notes:** [NOTE FOR PM: the mechanism by which development agents actually generate code — a custom tool-use loop vs. wrapping an existing coding-agent engine — is an open, unresolved technical decision. It doesn't change these FRs, but it's the highest-risk unknown in the whole product and deserves a dedicated spike before this feature is built. See §11.]

### 5.7 Automated QA
**Description:** Before anything is demoed, ProtoFlow validates the implementation against the original requirements and acceptance criteria — not just "does it run."

**Functional Requirements:**

#### FR-16: Generate and execute test cases from requirements
The system can generate test cases from the MVP's requirements and acceptance criteria, execute them, and record pass/fail with evidence.

#### FR-17: Report requirement coverage
The system can report, per requirement, whether it is covered by at least one test, and roll this up into overall coverage and pass/fail counts.
**Consequences (testable):**
- Every `MUST_HAVE` requirement has at least one mapped test before a Project can be marked demo-ready. [ASSUMPTION]

### 5.8 Demo Preparation
**Description:** ProtoFlow packages the validated MVP into something a consultant can run live for a client, without overclaiming what was actually built. Realizes UJ-1.

**Functional Requirements:**

#### FR-18: Generate a demo package
The system can generate a demo objective, step-by-step demo script, and synthetic demo data (clearly marked as synthetic) for the validated MVP.

#### FR-19: Honestly represent implementation status
Every capability shown in a demo is labeled `IMPLEMENTED`, `SIMULATED`, or `NOT_IMPLEMENTED`, and the system never presents simulated functionality as production functionality.
**Consequences (testable):**
- The demo script and the demo package agree on status labels — no capability is scripted as if real when it's marked `SIMULATED`.

### 5.9 Project Workspace
**Description:** A consultant needs one place to see where a given client engagement stands across the whole pipeline.

**Functional Requirements:**

#### FR-20: View project status across all phases
A consultant can see, per Project, the current stage and status of Meeting, MVP, Design, Development, QA, and Demo at a glance.

## 6. Non-Goals (Explicit)
- ProtoFlow does not do project pricing, cost estimation, resource allocation, consultant/employee matching, or timeline estimation.
- ProtoFlow does not do full project planning, full production deployment management, billing, or contract generation.
- ProtoFlow is not a complete enterprise project-management tool, and does not manage complex CI/CD, Kubernetes, or multi-cloud infrastructure.
- ProtoFlow does not autonomously deploy anything to production — human review gates code (§5.6) the same way it gates scope (§5.4).
- ProtoFlow is not a general-purpose "prompt to app" builder — every feature it proposes must trace back to an actual client conversation, not an open-ended prompt.
- [NON-GOAL for MVP] ProtoFlow does not support multiple concurrent users/teams on one deployment, or client-facing login — see §3.2.

## 7. MVP Scope

### 7.1 In Scope
- Simulated meeting ingestion via a mock provider, with multiple realistic transcript-quality fixtures
- Meeting Intelligence extraction with evidence traceability and confidence scoring
- Scope-constrained MVP proposal and versioning
- Human approval gate (approve/reject/edit/request revision)
- Lightweight UX + technical design generation
- AI-assisted implementation against a real Git repository, producing a PR
- Automated QA with requirement coverage reporting
- Honest demo package generation
- A single-project workspace view across all phases

### 7.2 Out of Scope for MVP
- Real meeting-platform integration (live Jitsi/JaaS or otherwise) — deferred; the mock provider fully stands in for v1. [NOTE FOR PM: revisit once the mocked pipeline is proven end-to-end; leaning self-hosted over a paid provider, not yet decided.]
- Multi-user/team accounts, client-facing login
- Everything listed in §6 (pricing, estimation, PM, deployment automation, etc.)
- Semantic/historical project search across past engagements (the spec's future "Project Intelligence" layer) — deferred to v2+.

## 8. Cross-Cutting NFRs
- **Performance:** notification/webhook handling responds in under 2 seconds; all AI processing is asynchronous.
- **Reliability:** every asynchronous job (transcript processing, intelligence extraction, MVP analysis, design, code generation, QA, demo prep) has a `PENDING`/`RUNNING`/`COMPLETED`/`FAILED` lifecycle with retry and a surfaced error reason.
- **Idempotency:** the same meeting-completion notification, delivered more than once, results in processing exactly once.
- **Auditability:** structured logs exist for every major processing event (what happened, for which project/meeting, how long it took, what was produced).

## 9. Constraints and Guardrails

**Safety**
- AI-inferred information is never presented as a client-confirmed requirement. Every important extracted item carries evidence or an explicit `INFERRED`/`NEEDS_REVIEW` marking (§5.2).
- Generated/untrusted code never executes outside an isolated environment (§5.6).
- Nothing proceeds past the Human Approval Gate (§5.4) or a code review/PR step (§5.6) automatically.

**Privacy**
- [ASSUMPTION] Client meeting transcripts may contain sensitive business information; in v1 (single-operator, self-hosted/dev environment) this is managed by keeping data local rather than by formal access-control features — revisit if ProtoFlow ever moves beyond single-operator use.

**Cost**
- [ASSUMPTION] LLM API cost is a real but secondary concern for a solo user at v1 scale; no budget/quota enforcement is required for v1, but the LLM access layer should not make provider switching (e.g. to a cheaper model) require rework — mechanism detail in `addendum.md`.

## 10. Success Metrics

**Primary**
- **SM-1**: A single simulated client meeting flows through the entire pipeline — transcript → intelligence → approved MVP → design → generated code (PR) → QA → demo package — without manual data-fixing along the way. Validates FR-1 through FR-19.

**Secondary**
- **SM-2**: 100% of requirements extracted from each of the 5 mock transcripts either carry valid evidence or are explicitly marked `INFERRED`/`NEEDS_REVIEW`. Validates FR-5, FR-7.
- **SM-3**: Every `MUST_HAVE` requirement in an approved MVP has at least one passing or explicitly failing mapped test in the QA Report. Validates FR-17.

**Counter-metrics (do not optimize)**
- **SM-C1**: Number of features/requirements proposed in an MVP. A larger MVP is not success — the goal is the smallest useful demoable product, not the most complete one. Counterbalances any temptation to treat "more extracted/proposed" as better.

## 11. Open Questions
1. How should development agents actually generate code — a custom tool-use loop, or wrapping an existing coding-agent engine (e.g. Claude Agent SDK, Aider, OpenHands)? Unresolved; deserves a dedicated spike before §5.6 is built.
2. Real meeting provider target for a future phase: self-hosted Jitsi+Jigasi vs. JaaS. Leaning self-hosted; not committed.
3. Does ProtoFlow ever need multi-user/team support, or does it stay single-operator indefinitely?

## 12. Assumptions Index
- §3 (intro): ProtoFlow v1 has exactly one user type (the solo consultant); no multi-seat/team model; the client never logs in directly.
- §3.2: Multi-tenant/shared use is a Non-User for v1.
- §5.1: Meeting provider is pluggable by design, mock-only for v1 (full detail in `addendum.md`).
- §5.7 FR-17: Every `MUST_HAVE` requirement needs at least one mapped test before demo-ready.
- §7.2: Real meeting-platform integration is deferred past v1 scope.
- §9 Privacy: Local-data-only handling is sufficient for v1's single-operator scope.
- §9 Cost: No budget/quota enforcement needed at v1 scale, but provider-switching flexibility is still required.
