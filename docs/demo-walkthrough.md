# End-to-End Demo Walkthrough (Epic 9)

This is the full ProtoFlow success scenario (SM-1): a single simulated client meeting flows all the
way to a demo package, with no manual data-fixing along the way. It runs offline on the deterministic
`mock` LLM and `mock` coding engine — no API keys required.

## Run it via the API

Bring the stack up (`docker compose up --build`), then, with `PID` = a project id:

```bash
# 1. Create a project
curl -s -X POST localhost:8000/api/v1/projects -H 'content-type: application/json' \
  -d '{"name":"Acme"}'                                   # -> {"id": "<PID>", ...}

# 2. Simulate a meeting (creates the meeting + emits transcript-ready through the real path)
curl -s -X POST localhost:8000/api/v1/dev/simulate-meeting -H 'content-type: application/json' \
  -d '{"project_id":"<PID>","fixture":"clean"}'

# The worker then runs transcript -> intelligence automatically. Or drive the phases directly:
curl -s -X POST localhost:8000/api/v1/projects/<PID>/mvp          # 4. propose MVP
curl -s -X POST localhost:8000/api/v1/projects/<PID>/mvp/approve \
  -H 'content-type: application/json' \
  -d '{"version":1,"action":"APPROVE","approved_by":"me"}'        # 5. human approval
curl -s -X POST localhost:8000/api/v1/projects/<PID>/design       # 6. design
curl -s -X POST localhost:8000/api/v1/projects/<PID>/code         # 7. code + PR
curl -s -X POST localhost:8000/api/v1/projects/<PID>/qa           # 8. QA
curl -s -X POST localhost:8000/api/v1/projects/<PID>/demo         # 9. demo package

# Cross-phase status at any time (FR-20):
curl -s localhost:8000/api/v1/projects/<PID>/overview
```

## Run it in the UI

Open http://localhost:5173, create a project, then walk the left-nav tabs top to bottom:
**Overview → Meetings → Intelligence → MVP → Design → Development → QA → Demo**. The Overview tab
shows each phase flip to *Complete* as you go.

## Expected output

- **Intelligence:** requirements/personas/constraints/decisions/risks with evidence.
- **MVP:** objective, MUST/SHOULD/NICE features, acceptance criteria — approvable.
- **Design:** screens, components, APIs, data model, tech decisions.
- **Development:** ordered task plan, generated files, and a pull-request URL.
- **QA:** per-feature coverage, pass/fail counts, `demo_ready = true`.
- **Demo:** objective, script, `SYNTHETIC`-marked data, and honest
  `IMPLEMENTED`/`SIMULATED`/`NOT_IMPLEMENTED` capability labels derived from QA.

## Automated proof

`backend/app/tests/test_e2e.py::test_full_pipeline_runs_end_to_end` runs this entire chain in one
test and asserts every phase produced real output and the overview reports all phases complete.

## Going live

Swap the mocks for real providers via `.env` (all default to mock/offline):

- `LLM_PROVIDER=ollama|openai` (+ keys) — meeting/MVP/design intelligence.
- `DEV_LLM_PROVIDER=…` — the developer team's model (Dev Manager, QA, Demo).
- `CODING_ENGINE=claude` (+ `ANTHROPIC_API_KEY`) — real code generation via the Claude Agent SDK.
- `GIT_PUBLISHER=github` (+ `GITHUB_TOKEN`, `GITHUB_REPO`) — open a real PR.
- `SANDBOX_MODE=docker` — run generated code in a network-less container.
- `LANGSMITH_TRACING=true` (+ key) — trace every chain run.
