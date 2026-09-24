# ProtoFlow — AI-Powered Client-to-MVP Platform

> **Status:** Initial MVP Technical Specification
> **Purpose:** Coding-agent implementation document
> **Primary goal:** Turn a client meeting into a working MVP that can be demonstrated to the client.

---

# 1. Product Overview

## 1.1 Product Name

**ProtoFlow**

### Tagline

> **From Client Meeting to Working MVP**

Alternative:

> **AI-Powered Client-to-MVP Platform**

---

## 1.2 Problem

In a typical software consulting/project development process:

```text
Client Meeting
      ↓
Meeting Notes
      ↓
BA Analysis
      ↓
Requirements
      ↓
PRD / SRD
      ↓
MVP Definition
      ↓
UX / Solution Design
      ↓
Development
      ↓
Testing
      ↓
Demo
```

This process can take days or weeks before the client sees something tangible.

ProtoFlow aims to compress this cycle.

The target workflow is:

```text
Client Meeting
      ↓
Automatic Transcript
      ↓
Meeting Intelligence
      ↓
MVP Definition
      ↓
Human Approval
      ↓
MVP Design
      ↓
AI Development Team
      ↓
QA
      ↓
Working MVP
      ↓
Client Demo
```

The system should behave like an **AI product/project team** that assists humans throughout the discovery-to-demo process.

---

# 2. Core Product Vision

The core question ProtoFlow should answer is:

> **"After talking to this client, what is the smallest useful product we can build and demonstrate?"**

The system should NOT initially attempt to generate an entire enterprise project.

It should optimize for:

* understanding the client
* identifying the actual problem
* extracting requirements
* defining a small MVP
* designing the MVP
* implementing the MVP
* testing the MVP
* preparing a client demo

---

# 3. Critical Scope Boundary

## 3.1 In Scope

The initial product should cover:

1. Meeting ingestion
2. Transcript ingestion
3. Meeting intelligence
4. Requirement extraction
5. Requirement traceability
6. MVP definition
7. MVP scope analysis
8. Human approval
9. MVP UX/design definition
10. Lightweight technical design
11. AI-assisted development
12. Automated testing
13. MVP validation
14. Demo preparation

---

## 3.2 Explicitly Out of Scope

**Do NOT implement these in the initial MVP:**

* project pricing
* project cost estimation
* resource allocation
* employee availability
* consultant matching
* timeline estimation
* full project planning
* full production deployment management
* billing
* contract generation
* complete enterprise project management
* complex CI/CD infrastructure
* Kubernetes
* multi-cloud deployment
* autonomous production deployment

These can be implemented in future phases.

---

# 4. Long-Term Product Roadmap

ProtoFlow should eventually evolve into:

```text
                    ┌─────────────────────┐
                    │    Client Meeting   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Meeting Intelligence│
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   MVP Definition   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │    MVP Design      │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   MVP Development  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │        QA           │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │    Client Demo      │
                    └──────────┬──────────┘
                               ↓
             ┌─────────────────┴─────────────────┐
             ↓                                   ↓
      Estimation & Pricing                Full Delivery
             ↓                                   ↓
      Resource Planning                 Project Management
```

The current implementation stops after:

```text
Client Meeting → Working MVP → Client Demo
```

---

# 5. High-Level Architecture

## 5.1 Architecture

Use an event-driven architecture.

```text
┌──────────────────────┐
│       Jitsi          │
│   Client Meeting     │
└──────────┬───────────┘
           │
           │ Transcript Ready
           ↓
┌──────────────────────┐
│ Webhook/Event API    │
│      FastAPI         │
└──────────┬───────────┘
           │
           │ enqueue job
           ↓
┌──────────────────────┐
│     Job Queue        │
│       Redis          │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Transcript Service   │
└──────────┬───────────┘
           │
           ↓
┌────────────────────────────┐
│   Meeting Intelligence     │
│       LangGraph            │
└──────────┬─────────────────┘
           │
           ↓
┌────────────────────────────┐
│      MVP Definition        │
│        Agent Team          │
└──────────┬─────────────────┘
           │
           ↓
      Human Approval
           │
           ↓
┌────────────────────────────┐
│       MVP Design           │
│        Agent Team           │
└──────────┬─────────────────┘
           │
           ↓
┌────────────────────────────┐
│    AI Development Team     │
└──────────┬─────────────────┘
           │
           ↓
┌────────────────────────────┐
│           QA               │
└──────────┬─────────────────┘
           │
           ↓
┌────────────────────────────┐
│      Working MVP           │
└──────────┬─────────────────┘
           │
           ↓
┌────────────────────────────┐
│     Demo Preparation       │
└────────────────────────────┘
```

---

# 6. Recommended Technology Stack

## 6.1 Frontend

Use:

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui
* React Query

---

## 6.2 Backend

Use:

* Python 3.12+
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

---

## 6.3 AI

Use:

* LangGraph
* LangChain where appropriate
* Pydantic structured output
* configurable LLM provider

The application must not hard-code a single LLM provider.

Create an abstraction such as:

```python
class LLMProvider:
    ...
```

The system should support OpenAI-compatible APIs.

Potential providers:

* OpenAI
* Azure AI Foundry
* local OpenAI-compatible models

---

## 6.4 Database

Use:

* PostgreSQL

PostgreSQL is the primary system of record.

---

## 6.5 Vector Database

Use:

* Qdrant

However, do not introduce vector search everywhere unnecessarily.

Qdrant should initially be used only where semantic retrieval provides clear value.

Potential future use:

* historical project knowledge
* project documents
* meeting history
* reusable solution patterns
* previous MVPs

---

## 6.6 Queue

Use:

* Redis

Redis should be used for asynchronous processing.

---

## 6.7 Object Storage

For local development:

* MinIO

Future:

* Azure Blob Storage

Use object storage for:

* transcripts
* uploaded documents
* generated artifacts
* source files
* generated code packages

---

## 6.8 Meeting Provider

Initial provider:

**Jitsi / JaaS**

Create a provider abstraction so that other providers can later be added.

Potential future providers:

* Zoom
* Microsoft Teams
* Google Meet

---

## 6.9 Observability

Initial:

* structured application logs
* LangSmith

Future:

* OpenTelemetry
* Prometheus
* Grafana
* Azure Application Insights

---

## 6.10 Evaluation

Use:

* RAGAS where appropriate
* custom evaluation metrics
* LLM-as-judge where appropriate
* human evaluation

Meeting intelligence should especially be evaluated for:

* requirement extraction accuracy
* hallucination
* missing requirements
* evidence accuracy
* speaker attribution
* confidence calibration

---

# 7. Core Domain Model

The following objects should exist in the system.

---

# 8. Project

A Project represents a client/product initiative.

Example:

```json
{
  "id": "project_001",
  "name": "AI Customer Support Platform",
  "description": "AI-powered customer support solution",
  "status": "DISCOVERY"
}
```

Possible statuses:

```text
DISCOVERY
MVP_DEFINITION
DESIGN
DEVELOPMENT
QA
DEMO_READY
COMPLETED
```

---

# 9. Meeting

A meeting belongs to a project.

Suggested model:

```python
Meeting:
    id
    project_id
    provider
    external_meeting_id
    title
    start_time
    end_time
    participants
    status
    created_at
    updated_at
```

Possible statuses:

```text
SCHEDULED
IN_PROGRESS
COMPLETED
TRANSCRIPT_PENDING
TRANSCRIPT_READY
PROCESSING
PROCESSED
FAILED
```

---

# 10. Transcript

A transcript contains the raw and normalized meeting conversation.

```python
Transcript:
    id
    meeting_id
    raw_content
    normalized_content
    language
    status
    created_at
```

Transcript segments:

```python
TranscriptSegment:
    speaker
    start_time
    end_time
    text
```

Example:

```json
{
  "speaker": "Client",
  "start_time": 1892,
  "end_time": 1910,
  "text": "Most of our documents are Vietnamese."
}
```

---

# 11. Meeting Event

Meeting events must be idempotent.

```python
MeetingEvent:
    id
    provider
    event_type
    external_event_id
    meeting_id
    payload
    received_at
    processed_at
    status
```

Statuses:

```text
RECEIVED
QUEUED
PROCESSING
COMPLETED
FAILED
```

The same webhook must never trigger duplicate processing.

Use:

```text
provider + external_event_id
```

as an idempotency key.

---

# 12. Processing Job

```python
ProcessingJob:
    id
    project_id
    meeting_id
    job_type
    status
    attempt_count
    error_message
    started_at
    completed_at
```

Possible job types:

```text
TRANSCRIPT_PROCESSING
MEETING_INTELLIGENCE
MVP_ANALYSIS
MVP_DESIGN
CODE_GENERATION
QA
DEMO_PREPARATION
```

---

# 13. Meeting Intelligence

The Meeting Intelligence system converts raw conversation into structured project knowledge.

---

## 13.1 Required Output

The agent should extract:

### Client Context

* client/company
* industry
* business area
* existing product/system
* relevant organizational context

### Business Problem

* current problem
* pain points
* root causes where explicitly discussed
* business impact

### Desired Outcome

* business goals
* expected outcomes
* success criteria

### Users

* user personas
* user roles
* target customers
* internal users

### Requirements

* functional requirements
* non-functional requirements
* integrations
* data requirements
* UI requirements

### Constraints

* technical constraints
* regulatory constraints
* security requirements
* timeline constraints if mentioned
* existing technology constraints

### Existing Systems

* current applications
* databases
* APIs
* third-party services
* legacy systems

### Decisions

Capture decisions explicitly made during the meeting.

### Open Questions

Capture things that are unclear or require clarification.

### Assumptions

Clearly distinguish assumptions from confirmed requirements.

### Risks

Identify risks mentioned or directly implied by requirements.

### Action Items

Capture:

* action
* owner
* deadline if mentioned

---

# 14. Requirement Traceability

This is a critical ProtoFlow feature.

Every important extracted requirement should maintain evidence.

Example:

```json
{
  "requirement_id": "REQ-012",
  "description": "The system must support Vietnamese documents.",
  "type": "functional",
  "priority": "HIGH",
  "status": "CONFIRMED",
  "source": {
    "meeting_id": "meeting_001",
    "speaker": "Client",
    "start_time": "00:31:42",
    "end_time": "00:31:55",
    "quote": "Most of our documents are Vietnamese."
  },
  "confidence": 0.96
}
```

The system should allow users to navigate:

```text
Requirement
    ↓
Meeting Evidence
    ↓
Transcript Timestamp
```

This is important because AI-generated requirements must be auditable.

---

# 15. Explicit vs Inferred Requirements

The system must distinguish between:

```text
EXPLICIT
```

and

```text
INFERRED
```

Example:

Client says:

> "Customers should be able to upload documents and ask questions."

Explicit requirements:

```text
REQ-001 Upload documents
REQ-002 Ask questions
```

Potential inferred requirement:

```text
REQ-003 Document processing
```

REQ-003 should be marked:

```text
INFERRED
```

and should not be presented as confirmed client scope.

---

# 16. Meeting Intelligence Agent Architecture

Use LangGraph.

Recommended flow:

```text
Transcript
    ↓
Preprocessing
    ↓
Conversation Segmentation
    ↓
Business Context Agent
    ↓
Requirement Extraction Agent
    ↓
User/Persona Agent
    ↓
Constraint Agent
    ↓
Decision Agent
    ↓
Open Question Agent
    ↓
Risk Agent
    ↓
Evidence Validator
    ↓
Meeting Intelligence Synthesizer
```

---

# 17. Evidence Validator

The Evidence Validator should verify:

1. Every important requirement has evidence.
2. Evidence actually supports the requirement.
3. Speaker is correctly attributed.
4. Timestamp exists.
5. Inferred information is marked as inferred.
6. Confidence is assigned.

If evidence is weak:

```text
status = NEEDS_REVIEW
```

---

# 18. MVP Definition Agent Team

After Meeting Intelligence, ProtoFlow should determine:

> "What is the smallest useful MVP we can show this client?"

Do NOT generate a complete enterprise PRD.

The output should be intentionally small.

---

## 18.1 Agent Team

### MVP Product Manager

Responsibilities:

* define MVP objective
* identify business value
* identify target user
* propose smallest useful product

---

### Feature Analyst

Responsibilities:

* convert requirements into candidate features
* identify dependencies
* identify feature priorities

---

### UX Analyst

Responsibilities:

* identify core user journey
* identify required screens
* remove unnecessary UX

---

### MVP Scope Analyst

Responsibilities:

* aggressively reduce scope
* identify must-have features
* identify nice-to-have features
* identify out-of-scope features

---

### MVP Critic

Responsibilities:

* challenge proposed scope
* identify unnecessary features
* detect scope creep
* identify missing critical functionality
* check demo viability

---

### MVP Synthesizer

Produces the final MVP specification.

---

# 19. MVP Specification

This is the **central data contract** of ProtoFlow.

Everything after this stage should use the MVP Specification.

Structure:

```python
MVPSpecification:
    project_id

    problem
    business_context

    target_users
    goals

    features
    user_journeys

    ui_requirements
    technical_constraints

    acceptance_criteria

    out_of_scope
    assumptions
    open_questions

    demo_scenario

    requirement_traceability
```

---

# 20. Example MVP

Suppose the client describes:

> "We want an AI customer support platform."

A full enterprise system could contain:

```text
Authentication
CRM integration
Knowledge management
AI chatbot
Analytics
Agent escalation
Admin dashboard
User management
Billing
Audit logs
Multilingual support
Notifications
Customer history
```

ProtoFlow should NOT automatically build all of this.

The MVP could become:

```text
1. Upload knowledge documents
2. Process documents
3. Ask questions
4. Retrieve relevant information
5. Generate answer
6. Show source citations
```

Demo flow:

```text
Upload document
      ↓
Ask question
      ↓
Retrieve relevant information
      ↓
AI answer
      ↓
Show source
```

---

# 21. MVP Scope Classification

Every feature must be classified:

```text
MUST_HAVE
SHOULD_HAVE
NICE_TO_HAVE
OUT_OF_SCOPE
```

Initial MVP should normally contain only:

```text
MUST_HAVE
```

and a small number of:

```text
SHOULD_HAVE
```

if required for the demo.

---

# 22. Human Approval Gate

The MVP definition MUST NOT automatically proceed to development.

Human approval is required.

Workflow:

```text
AI MVP Proposal
       ↓
Human Review
       ↓
Edit / Reject / Approve
       ↓
Approved MVP
       ↓
Design
```

UI should provide:

```text
Approve
Reject
Edit
Request Revision
```

Approval should be persisted.

Example:

```python
MVPApproval:
    id
    project_id
    version
    approved_by
    approved_at
    comments
```

---

# 23. MVP Versioning

MVP specifications should be versioned.

Example:

```text
MVP v0.1
MVP v0.2
MVP v0.3
MVP v1.0 APPROVED
```

Never overwrite approved versions.

---

# 24. MVP Design Phase

Input:

```text
Approved MVP Specification
```

Output:

```text
UX Flow
+
Screen Definition
+
Lightweight Technical Design
```

---

# 25. UX Agent

The UX Agent generates:

* user journey
* screen list
* navigation
* interactions
* important UI states

Example:

```text
Dashboard
    ↓
Document Upload
    ↓
Processing
    ↓
Chat
    ↓
Answer + Sources
```

---

# 26. Solution Design Agent

Generate a lightweight technical architecture.

Example:

```text
React
  ↓
FastAPI
  ↓
AI Service
  ↓
Vector Database
  ↓
Document Storage
```

The output should include:

* components
* APIs
* data model
* AI workflow
* integrations
* technology decisions

Do NOT generate a huge architecture document.

Target:

```text
1–5 pages equivalent
```

---

# 27. MVP Development Team

The MVP development team should operate against a real Git repository.

Recommended repository:

```text
GitHub
```

---

# 28. Development Agents

## Development Manager

Responsibilities:

* inspect MVP specification
* break requirements into tasks
* define implementation order
* coordinate development agents
* validate implementation completeness

---

## Frontend Developer Agent

Responsibilities:

* React
* TypeScript
* UI
* API integration
* state management
* user interaction

---

## Backend Developer Agent

Responsibilities:

* FastAPI
* API endpoints
* database
* business logic
* integrations

---

## AI Engineer Agent

Responsibilities:

* LLM integration
* prompts
* RAG
* LangGraph workflows
* structured outputs
* AI evaluation

---

## QA Agent

Responsibilities:

* generate test cases
* run tests
* validate requirements
* identify defects
* verify acceptance criteria

---

# 29. Development Workflow

```text
Approved MVP
     ↓
Development Manager
     ↓
Task Breakdown
     ↓
Repository Inspection
     ↓
Implementation Plan
     ↓
Frontend / Backend / AI Development
     ↓
Automated Tests
     ↓
QA Agent
     ↓
Fix Issues
     ↓
Final Validation
     ↓
Working MVP
```

---

# 30. Example Task Breakdown

For a document Q&A MVP:

```text
EPIC: Document Q&A

TASK-001 Create upload page
TASK-002 Create upload API
TASK-003 Store uploaded document
TASK-004 Extract document text
TASK-005 Chunk document
TASK-006 Generate embeddings
TASK-007 Store embeddings
TASK-008 Implement retrieval
TASK-009 Implement answer generation
TASK-010 Implement source citation
TASK-011 Create chat UI
TASK-012 Add automated tests
TASK-013 QA validation
```

---

# 31. Coding Agent Requirements

Coding agents must:

1. Inspect existing repository before modifying it.
2. Understand architecture before writing code.
3. Avoid unnecessary rewrites.
4. Follow existing coding conventions.
5. Write tests.
6. Keep changes focused.
7. Explain implementation decisions.
8. Never silently modify requirements.
9. Never invent missing business requirements.
10. Flag ambiguity for human review.

---

# 32. Human Approval Before Merge

The system should eventually support:

```text
AI-generated code
       ↓
Tests
       ↓
QA
       ↓
Human Review
       ↓
Merge
```

For the initial prototype, GitHub PR creation is sufficient.

Autonomous production deployment is out of scope.

---

# 33. QA System

QA should validate the MVP against:

```text
Requirements
Acceptance Criteria
User Journey
Technical Design
```

Example:

```text
REQ-001
  ↓
Acceptance Criteria
  ↓
Test Case
  ↓
Execution
  ↓
PASS / FAIL
```

---

# 34. Requirement-to-Test Traceability

ProtoFlow should eventually provide:

```text
Requirement
    ↓
Feature
    ↓
Implementation Task
    ↓
Code
    ↓
Test
    ↓
Demo Scenario
```

This creates an end-to-end traceability chain.

Example:

```text
REQ-001
"User can upload PDF"

        ↓

FEATURE-001
"Document Upload"

        ↓

TASK-001
"Create upload API"

        ↓

TEST-001
"Upload PDF successfully"

        ↓

DEMO-001
"Upload customer document"
```

---

# 35. Client Demo Preparation

Once the MVP passes QA:

```text
Working MVP
     ↓
Demo Preparation Agent
     ↓
Client Demo Package
```

Generate:

### Demo Objective

What should the client understand after the demo?

### Demo Script

Example:

```text
1. Introduce the problem
2. Upload sample document
3. Ask question
4. Show AI answer
5. Show source citation
6. Explain value
7. Explain current MVP limitations
8. Discuss next steps
```

---

# 36. Demo Data

The Demo Agent should generate or recommend:

* sample documents
* sample users
* sample questions
* sample records
* realistic test scenarios

All generated demo data must clearly be marked as synthetic where appropriate.

---

# 37. Honest Demo Representation

ProtoFlow must clearly distinguish:

```text
IMPLEMENTED
```

```text
SIMULATED
```

```text
NOT IMPLEMENTED
```

Example:

```text
Authentication
Status: SIMULATED
```

or:

```text
CRM Integration
Status: NOT IMPLEMENTED
```

The system must never claim that simulated functionality is production functionality.

---

# 38. Project Workspace

The frontend should provide a project workspace.

Example:

```text
ProtoFlow
│
├── Projects
│
└── AI Customer Support
      │
      ├── Overview
      ├── Meetings
      ├── Intelligence
      ├── MVP
      ├── Design
      ├── Development
      ├── QA
      └── Demo
```

---

# 39. Project Overview Page

Show:

```text
Project
Client
Current Stage
Latest Meeting
MVP Status
Development Status
QA Status
Demo Status
```

Example:

```text
AI Customer Support

Stage:
MVP DEVELOPMENT

Meeting:
Completed

MVP:
Approved

Design:
Completed

Development:
In Progress

QA:
Pending

Demo:
Pending
```

---

# 40. Meetings Page

Show:

```text
Meeting List

Meeting title
Date
Participants
Duration
Transcript status
AI processing status
```

Selecting a meeting should show:

```text
Transcript
+
Meeting Intelligence
+
Requirements
+
Decisions
+
Open Questions
+
Action Items
```

---

# 41. Intelligence Page

Sections:

```text
Business Context
Problem
Goals
Users
Requirements
Constraints
Decisions
Risks
Open Questions
Action Items
```

Requirements should show evidence.

Example:

```text
REQ-012

System must support Vietnamese documents.

Priority:
HIGH

Source:
Client

Timestamp:
00:31:42

Confidence:
96%

[View Evidence]
```

---

# 42. MVP Page

Display:

```text
MVP Objective

Target Users

Core User Journey

Features

Must Have

Should Have

Out of Scope

Assumptions

Open Questions

Acceptance Criteria

Demo Scenario
```

Actions:

```text
Edit
Approve
Request Revision
View Version
```

---

# 43. Design Page

Show:

```text
User Journey

Screens

Architecture

Components

APIs

Data Model

Technical Decisions
```

---

# 44. Development Page

Show:

```text
Epics
Tasks
Agent
Status
Pull Requests
Tests
Build Status
```

Example:

```text
TASK-001
Create upload page

Agent:
Frontend Developer

Status:
COMPLETED
```

---

# 45. QA Page

Show:

```text
Total Tests
Passed
Failed
Blocked

Requirement Coverage
Acceptance Criteria Coverage
```

Example:

```text
Tests: 25

Passed: 23
Failed: 2
Blocked: 0

Requirement Coverage: 100%
```

---

# 46. Demo Page

Show:

```text
Demo Objective

Demo Script

Demo Data

Implemented Features

Simulated Features

Known Limitations

Next Steps
```

Provide:

```text
Start Demo
```

where appropriate.

---

# 47. API Architecture

Use REST APIs initially.

Example:

```text
/api/v1/projects
/api/v1/projects/{project_id}

/api/v1/projects/{project_id}/meetings
/api/v1/meetings/{meeting_id}

/api/v1/meetings/{meeting_id}/transcript
/api/v1/meetings/{meeting_id}/intelligence

/api/v1/projects/{project_id}/mvp
/api/v1/projects/{project_id}/mvp/approve

/api/v1/projects/{project_id}/design

/api/v1/projects/{project_id}/development
/api/v1/projects/{project_id}/tasks

/api/v1/projects/{project_id}/qa

/api/v1/projects/{project_id}/demo
```

Webhook:

```text
POST /api/v1/webhooks/jitsi
```

---

# 48. Meeting Provider Abstraction

Do not tightly couple business logic to Jitsi.

Create an abstraction such as:

```python
class MeetingProvider(Protocol):

    async def get_meeting(
        self,
        meeting_id: str
    ):
        ...

    async def get_transcript(
        self,
        meeting_id: str
    ):
        ...

    async def verify_webhook(
        self,
        request
    ):
        ...
```

Implementation:

```text
MeetingProvider
      │
      ├── JitsiMeetingProvider
      ├── ZoomMeetingProvider       future
      ├── TeamsMeetingProvider      future
      └── GoogleMeetProvider        future
```

---

# 49. Webhook Design

The webhook must be lightweight.

Correct:

```text
Jitsi
 ↓
Webhook
 ↓
Validate
 ↓
Persist Event
 ↓
Queue Job
 ↓
Return 200
```

Incorrect:

```text
Jitsi
 ↓
Webhook
 ↓
Run LLM
 ↓
Process transcript
 ↓
Generate MVP
 ↓
Return response
```

Never run long-running AI operations directly inside the webhook request.

---

# 50. Event Processing

Use:

```text
Webhook
   ↓
Event Store
   ↓
Redis Queue
   ↓
Worker
   ↓
Processing
```

Workers should support:

* retry
* failure handling
* idempotency
* logging

---

# 51. LangGraph Architecture

Use LangGraph for agent orchestration.

Example:

```text
START
  ↓
load_transcript
  ↓
segment_conversation
  ↓
extract_business_context
  ↓
extract_requirements
  ↓
extract_personas
  ↓
extract_constraints
  ↓
extract_decisions
  ↓
extract_open_questions
  ↓
extract_risks
  ↓
validate_evidence
  ↓
synthesize_intelligence
  ↓
END
```

MVP graph:

```text
Meeting Intelligence
       ↓
MVP Product Manager
       ↓
Feature Analyst
       ↓
UX Analyst
       ↓
Scope Analyst
       ↓
MVP Critic
       ↓
MVP Synthesizer
       ↓
Human Approval
```

---

# 52. Agent State

Use typed state.

Example:

```python
class MeetingIntelligenceState(TypedDict):
    project_id: str
    meeting_id: str
    transcript: list[TranscriptSegment]

    business_context: BusinessContext
    requirements: list[Requirement]
    personas: list[Persona]
    constraints: list[Constraint]

    decisions: list[Decision]
    risks: list[Risk]
    open_questions: list[OpenQuestion]
    action_items: list[ActionItem]

    validation_errors: list[str]
```

---

# 53. Structured Outputs

All important AI outputs must use structured schemas.

Do NOT rely on free-form LLM responses for system-critical objects.

Use:

```text
Pydantic models
```

Example:

```python
class Requirement(BaseModel):
    id: str
    description: str
    type: RequirementType
    priority: Priority
    status: RequirementStatus
    source: Evidence
    confidence: float
```

---

# 54. Confidence

Confidence should not be treated as absolute truth.

Use it as a review signal.

Example:

```text
0.90–1.00
High confidence

0.70–0.89
Medium confidence

< 0.70
Needs review
```

These thresholds should be configurable.

---

# 55. Prompt Engineering

Prompts should be stored separately from application logic.

Recommended:

```text
backend/
└── ai/
    └── prompts/
        ├── meeting_intelligence/
        │   ├── business_context.txt
        │   ├── requirements.txt
        │   ├── personas.txt
        │   └── synthesis.txt
        │
        └── mvp/
            ├── product_manager.txt
            ├── scope_analyst.txt
            ├── critic.txt
            └── synthesis.txt
```

Prompt versions should be traceable.

---

# 56. Project Memory

ProtoFlow should maintain persistent project knowledge.

At minimum:

```text
Project
 ├── Meetings
 ├── Transcripts
 ├── Intelligence
 ├── Requirements
 ├── Decisions
 ├── MVP Versions
 ├── Design
 ├── Development
 ├── QA
 └── Demo
```

Future:

```text
Project Memory
      ↓
Semantic Retrieval
      ↓
Relevant Historical Context
```

---

# 57. Future Project Intelligence Layer

Do not implement fully in Phase 1.

Eventually ProtoFlow should be able to answer:

```text
What did the client ask for last month?

Why was this decision made?

When did requirement X change?

What requirements are affected by this change?

What did the client reject?

What assumptions are still unresolved?
```

This becomes the long-term **Project Intelligence** layer.

---

# 58. Repository Structure

Recommended:

```text
ProtoFlow/
│
├── README.md
├── docker-compose.yml
├── .env.example
├── Makefile
│
├── backend/
│   ├── pyproject.toml
│   │
│   └── app/
│       ├── main.py
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── projects.py
│       │       ├── meetings.py
│       │       ├── transcripts.py
│       │       ├── intelligence.py
│       │       ├── mvp.py
│       │       ├── design.py
│       │       ├── development.py
│       │       ├── qa.py
│       │       ├── demo.py
│       │       └── webhooks.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── security.py
│       │
│       ├── db/
│       │   ├── database.py
│       │   ├── models/
│       │   └── migrations/
│       │
│       ├── domain/
│       │   ├── projects/
│       │   ├── meetings/
│       │   ├── intelligence/
│       │   ├── mvp/
│       │   ├── design/
│       │   ├── development/
│       │   ├── qa/
│       │   └── demo/
│       │
│       ├── ai/
│       │   ├── llm/
│       │   ├── graphs/
│       │   ├── agents/
│       │   ├── prompts/
│       │   ├── schemas/
│       │   └── evaluation/
│       │
│       ├── integrations/
│       │   ├── meetings/
│       │   │   ├── base.py
│       │   │   └── jitsi.py
│       │   ├── github/
│       │   └── storage/
│       │
│       ├── workers/
│       │   ├── queue.py
│       │   └── jobs/
│       │
│       └── tests/
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── features/
│   │   │   ├── projects/
│   │   │   ├── meetings/
│   │   │   ├── intelligence/
│   │   │   ├── mvp/
│   │   │   ├── design/
│   │   │   ├── development/
│   │   │   ├── qa/
│   │   │   └── demo/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── lib/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   └── scripts/
│
└── docs/
    ├── architecture.md
    ├── domain-model.md
    ├── api.md
    └── agents.md
```

---

# 59. Local Development

Use Docker Compose.

Services:

```text
frontend
backend
worker
postgres
redis
qdrant
minio
```

Potential architecture:

```text
                    Browser
                       │
                       ↓
                  React/Vite
                       │
                       ↓
                    FastAPI
                   /   |   \
                  /    |    \
                 ↓     ↓     ↓
          PostgreSQL Redis  Qdrant
                       │
                       ↓
                    Worker
                       │
                       ↓
                    LangGraph
                       │
                       ↓
                      LLM
```

---

# 60. Environment Variables

Use `.env`.

Example:

```env
APP_ENV=development

DATABASE_URL=
REDIS_URL=
QDRANT_URL=
MINIO_ENDPOINT=

LLM_PROVIDER=
OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=

LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=

JITSI_API_URL=
JITSI_API_KEY=
JITSI_WEBHOOK_SECRET=

GITHUB_TOKEN=
GITHUB_REPOSITORY=
```

Never commit secrets.

Provide:

```text
.env.example
```

---

# 61. Initial MVP Implementation Phases

## Phase 0 — Foundation

Implement:

* repository
* Docker Compose
* FastAPI
* React
* PostgreSQL
* Redis
* basic project model
* basic UI
* configuration
* logging
* health check

Acceptance:

```text
docker compose up
```

should start the system successfully.

---

# 62. Phase 1 — Meeting Integration

Implement:

```text
Jitsi
 ↓
Meeting
 ↓
Transcript
 ↓
Webhook
 ↓
Processing Job
```

Requirements:

* create meeting/project
* connect meeting to project
* receive transcript-ready event
* persist event
* retrieve transcript
* normalize transcript
* queue processing

Acceptance:

A completed meeting should eventually appear as:

```text
TRANSCRIPT_READY
```

and trigger processing automatically.

---

# 63. Phase 2 — Meeting Intelligence

Implement LangGraph workflow.

Input:

```text
Transcript
```

Output:

```text
Meeting Intelligence
```

Acceptance:

Given a test transcript, the system extracts:

* problem
* goals
* users
* requirements
* constraints
* decisions
* risks
* open questions
* action items

Every important requirement should contain evidence.

---

# 64. Phase 3 — MVP Definition

Implement:

```text
Meeting Intelligence
       ↓
MVP Agent Team
       ↓
MVP Specification
```

Acceptance:

The system generates:

* MVP objective
* target users
* core user journey
* features
* priorities
* out-of-scope
* assumptions
* acceptance criteria
* demo scenario

The output must remain MVP-sized.

---

# 65. Phase 4 — Human Approval

Implement:

```text
AI MVP
 ↓
Human Review
 ↓
Approve
```

Acceptance:

The system must prevent downstream design/development from starting until an MVP version is approved.

---

# 66. Phase 5 — MVP Design

Implement:

```text
Approved MVP
      ↓
UX Agent
      ↓
Solution Design Agent
```

Acceptance:

Generate:

* user journey
* screens
* architecture
* components
* APIs
* data model
* technical decisions

---

# 67. Phase 6 — AI Development

Implement:

```text
MVP Specification
      ↓
Development Manager
      ↓
Tasks
      ↓
Coding Agents
```

Initial version can use a simplified implementation approach.

The system should be capable of:

1. inspect repository
2. create task plan
3. generate code
4. generate tests
5. execute tests
6. identify failures
7. propose fixes

---

# 68. Phase 7 — QA

Implement:

```text
MVP Requirements
      ↓
Test Generation
      ↓
Test Execution
      ↓
QA Report
```

Acceptance:

The QA report should contain:

```text
Requirement
Test Case
Result
Evidence
Failure Reason
```

---

# 69. Phase 8 — Demo Preparation

Implement:

```text
Working MVP
      ↓
Demo Agent
      ↓
Demo Package
```

Acceptance:

Generate:

* demo objective
* demo script
* demo data
* implemented features
* simulated features
* known limitations
* next steps

---

# 70. Phase 9 — End-to-End Demo

The final demonstration should support this scenario:

```text
1. Create Project

2. Start Jitsi Meeting

3. Have client conversation

4. End meeting

5. Transcript automatically arrives

6. ProtoFlow processes transcript

7. Meeting Intelligence appears

8. Requirements are shown with evidence

9. AI generates MVP proposal

10. Human reviews MVP

11. Human approves MVP

12. AI generates MVP design

13. AI creates development tasks

14. Coding agents implement MVP

15. QA validates MVP

16. ProtoFlow generates demo package

17. User opens working MVP
```

This is the primary end-to-end success scenario.

---

# 71. Sample Demo Scenario

Use this as the initial test case.

## Client

A fictional company wants an AI document assistant.

## Meeting

Client says:

> We have hundreds of internal documents.

> Employees spend too much time searching for information.

> Most documents are PDF.

> Some documents are Vietnamese.

> We want employees to ask questions in natural language.

> The answer should show where the information came from.

> For the first demo, we only need a simple interface.

ProtoFlow should derive:

### Problem

Employees spend significant time searching internal documents.

### Users

Employees.

### MVP

```text
1. Upload PDF documents
2. Process documents
3. Ask natural-language questions
4. Retrieve relevant information
5. Generate answer
6. Display source citations
```

### Out of Scope

```text
SSO
Admin management
Analytics
CRM integration
Advanced permissions
Billing
Production deployment
```

### Demo

```text
Upload document
     ↓
Ask:
"What is the annual leave policy?"
     ↓
AI answer
     ↓
Source citation
```

---

# 72. Non-Functional Requirements

## Performance

Webhook response:

```text
< 2 seconds
```

Long-running AI operations must be asynchronous.

---

## Reliability

Jobs should support:

```text
retry
failure state
error logging
idempotency
```

---

## Security

Never:

* commit secrets
* log API keys
* expose credentials
* execute arbitrary generated code directly in production

Generated code execution should occur in an isolated environment.

---

# 73. AI Safety Requirements

The system must clearly distinguish:

```text
Client-confirmed information
```

from:

```text
AI inference
```

and:

```text
AI recommendation
```

Do not present AI assumptions as client requirements.

---

# 74. Hallucination Prevention

For meeting intelligence:

Every requirement should preferably have:

```text
Evidence
```

If evidence does not exist:

```text
source = null
status = INFERRED
```

or:

```text
status = NEEDS_REVIEW
```

---

# 75. Human-in-the-Loop Design

Humans should remain responsible for important decisions.

Approval gates:

```text
Meeting Intelligence
        ↓
Human review optional

MVP Definition
        ↓
Human approval REQUIRED

Technical Design
        ↓
Human review

Code
        ↓
Human review before merge

QA
        ↓
Human final validation

Demo
        ↓
Human launch
```

---

# 76. Error Handling

Every asynchronous operation must have:

```text
PENDING
RUNNING
COMPLETED
FAILED
```

Failure should expose:

```text
job ID
error message
timestamp
attempt count
```

Example:

```text
Meeting Intelligence

Status: FAILED

Reason:
LLM provider timeout

Attempt:
2 / 3

[Retry]
```

---

# 77. Logging

Use structured logs.

Example:

```json
{
  "event": "meeting_intelligence_completed",
  "project_id": "project_001",
  "meeting_id": "meeting_001",
  "duration_ms": 18234,
  "requirements_extracted": 12
}
```

---

# 78. Testing Strategy

## Backend

Use:

```text
pytest
```

Test:

* API
* database
* domain logic
* agent schemas
* workflow
* webhook
* event idempotency

---

## Frontend

Test:

* components
* page flows
* API integration
* approval flow

---

## AI

Maintain a small evaluation dataset.

Example:

```text
10–30 meeting transcripts
```

Each should contain expected:

* requirements
* decisions
* open questions
* personas

Track:

```text
precision
recall
faithfulness
evidence accuracy
```

---

# 79. Definition of Done

A feature is complete only when:

* implementation exists
* tests exist
* error handling exists
* logs exist
* API is documented
* UI is usable
* database migration exists if required
* no secrets are committed
* acceptance criteria are satisfied

---

# 80. Coding Standards

Use:

### Python

```text
ruff
black
mypy where practical
pytest
```

### TypeScript

```text
ESLint
Prettier
TypeScript strict mode
```

Use clear naming.

Prefer small modules.

Avoid large monolithic files.

---

# 81. Architecture Principles

The implementation must follow these principles:

## 1. Domain-first

Business logic should not be embedded directly in API routes.

Bad:

```python
@app.post("/mvp")
def create_mvp():
    # 500 lines of logic
```

Prefer:

```text
API
 ↓
Application Service
 ↓
Domain
 ↓
AI / Infrastructure
```

---

## 2. Provider abstraction

Do not couple the entire system to Jitsi.

---

## 3. AI abstraction

Do not couple the application to one LLM.

---

## 4. Asynchronous processing

Long-running AI work must be background jobs.

---

## 5. Structured outputs

Use schemas.

---

## 6. Traceability

AI-generated artifacts should maintain relationships to their sources.

---

## 7. Human approval

Important decisions require explicit approval.

---

## 8. Version everything important

Especially:

* MVP specification
* prompts
* AI outputs
* design
* generated code/task plans

---

# 82. Important Engineering Constraint

**Do not over-engineer the first version.**

Avoid initially introducing:

* Kubernetes
* microservices
* event buses with many topics
* complex IAM
* service mesh
* distributed tracing infrastructure
* complicated agent-to-agent protocols
* autonomous production deployment

Start with:

```text
React
FastAPI
PostgreSQL
Redis
Qdrant
MinIO
LangGraph
Jitsi
GitHub
```

A modular monolith + workers is preferred initially.

---

# 83. Suggested Implementation Order

The coding agent should implement in this order:

```text
1. Repository + Docker

2. Backend foundation

3. Database

4. Frontend foundation

5. Project management

6. Meeting model

7. Jitsi integration

8. Webhook

9. Transcript processing

10. Meeting Intelligence

11. Requirement traceability

12. MVP Agent Team

13. MVP UI

14. Human approval

15. MVP Design

16. Development task generation

17. GitHub integration

18. Coding agent

19. QA agent

20. Demo preparation

21. End-to-end integration
```

Do not start by building all agents simultaneously.

Build the pipeline incrementally.

---

# 84. Milestone Strategy

## Milestone 1

```text
Project
+
Meeting
+
Transcript
```

---

## Milestone 2

```text
Meeting
 ↓
Meeting Intelligence
```

---

## Milestone 3

```text
Meeting Intelligence
 ↓
MVP Specification
```

---

## Milestone 4

```text
MVP
 ↓
Human Approval
 ↓
Design
```

---

## Milestone 5

```text
MVP
 ↓
Development Tasks
 ↓
Generated Code
```

---

## Milestone 6

```text
Code
 ↓
QA
 ↓
Working MVP
```

---

## Milestone 7

```text
Working MVP
 ↓
Demo Package
```

---

# 85. Final MVP Success Criteria

ProtoFlow should be considered successful when the following scenario works:

```text
A user creates a project.

        ↓

The user creates/starts a Jitsi meeting.

        ↓

The user conducts a simulated client meeting.

        ↓

The meeting ends.

        ↓

The transcript becomes available.

        ↓

ProtoFlow automatically receives the transcript event.

        ↓

The transcript is processed asynchronously.

        ↓

Meeting Intelligence is generated.

        ↓

Requirements are displayed with evidence.

        ↓

ProtoFlow proposes a small MVP.

        ↓

The user reviews and approves it.

        ↓

ProtoFlow generates lightweight UX and technical design.

        ↓

Development tasks are generated.

        ↓

AI coding agents implement the MVP.

        ↓

QA validates the implementation.

        ↓

A working MVP is produced.

        ↓

ProtoFlow generates a client demo script.

        ↓

The user can demonstrate the MVP.
```

---

# 86. Future Phase — Estimation & Pricing

**Do not implement this now.**

Future architecture may include:

```text
Approved MVP
      ↓
Work Breakdown
      ↓
Historical Project Retrieval
      ↓
Resource Retrieval
      ↓
Effort Estimation
      ↓
Timeline Estimation
      ↓
Cost Estimation
      ↓
Pricing Recommendation
```

Potential future integrations:

```text
Internal Staff System
Project History
Historical Winning Bids
Resource MCP
Pricing MCP
```

This phase can eventually leverage ProtoFlow's project intelligence.

---

# 87. Future Phase — Full Project Delivery

Long-term:

```text
Client Meeting
      ↓
MVP
      ↓
Full PRD/SRD
      ↓
Architecture
      ↓
Project Plan
      ↓
Development
      ↓
QA
      ↓
Deployment
      ↓
Monitoring
      ↓
Maintenance
```

ProtoFlow could eventually become an:

> **AI-native project delivery platform for software consulting teams.**

But this is not part of the initial implementation.

---

# 88. Agent Operating Instructions

The coding agent should follow these rules throughout implementation:

### Rule 1

Read this specification before implementation.

### Rule 2

Do not implement features outside the current phase without explicit approval.

### Rule 3

Do not implement pricing or estimation.

### Rule 4

Do not treat inferred requirements as confirmed requirements.

### Rule 5

Maintain requirement traceability.

### Rule 6

Use structured AI outputs.

### Rule 7

Use asynchronous jobs for long-running AI processing.

### Rule 8

Make webhook processing idempotent.

### Rule 9

Keep provider-specific code isolated.

### Rule 10

Write tests for every major feature.

### Rule 11

Keep architecture simple enough for a single developer to maintain.

### Rule 12

Prioritize a working end-to-end flow over excessive abstraction.

---

# 89. First Development Task

Before implementing the entire system, create the foundation.

The first implementation should deliver:

```text
ProtoFlow
│
├── React frontend
│
├── FastAPI backend
│
├── PostgreSQL
│
├── Redis
│
├── Qdrant
│
├── MinIO
│
└── Docker Compose
```

Then implement:

```text
Create Project
      ↓
Create Meeting
      ↓
Store Meeting
```

Only after this foundation works should meeting provider integration begin.

---

# 90. Final Product Principle

The central principle of ProtoFlow is:

> **Do not try to automate the entire software development lifecycle at once. Automate the path from client conversation to a credible working MVP.**

The product should optimize for:

```text
UNDERSTAND
    ↓
DEFINE
    ↓
DESIGN
    ↓
BUILD
    ↓
TEST
    ↓
DEMO
```

rather than:

```text
MEETING
    ↓
100-PAGE PRD
    ↓
100-PAGE ARCHITECTURE
    ↓
6-MONTH PROJECT PLAN
```

The first product should prove one compelling capability:

> **A client can talk to us in the morning, and by the end of the workflow we have something tangible to show them.**

That is the core value proposition of ProtoFlow.
