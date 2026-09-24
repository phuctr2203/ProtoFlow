# ProtoFlow

> **From Client Meeting to Working MVP** — an AI-powered platform that turns a client discovery
> meeting into a demoable MVP.

ProtoFlow ingests a meeting transcript, extracts traceable requirements, proposes the smallest
useful MVP, gates it behind human approval, then designs, builds, QAs, and packages an honest demo.
See [`Idea.MD`](Idea.MD) for the full specification and [`docs/`](docs) for the delivery plan,
epics, and BMAD workflow guide.

## Tech stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2 — managed with `uv`
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, React Query — managed with `npm`
- **Infrastructure:** PostgreSQL, Redis, Docker Compose

## Quick start (Docker)

Bring up the whole stack (Postgres, Redis, backend, frontend):

```bash
cp .env.example .env
docker compose up --build      # or: make up
```

- Frontend: http://localhost:5173
- Backend API + docs: http://localhost:8000/api/v1 · http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

The backend runs `alembic upgrade head` on startup, so the database schema is created automatically.

## Local development (without Docker)

### Backend

```bash
cd backend
uv sync
uv run alembic upgrade head          # requires a running Postgres (see .env)
uv run uvicorn app.main:app --reload
uv run pytest                        # run tests
uv run ruff check . && uv run black --check .
```

### Frontend

```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173
npm test                             # run tests
npm run build                        # typecheck + production build
```

Copy `frontend/.env.example` to `frontend/.env` to point the app at a non-default backend URL.

## Make targets

| Target | Action |
|---|---|
| `make up` | Build and start the full stack via Docker Compose |
| `make down` | Stop the stack |
| `make migrate` | Apply database migrations |
| `make test` | Run backend + frontend tests |

## Project layout

```text
backend/    FastAPI service (api / core / db / domain / tests)
frontend/   React + Vite app (components / features / lib)
docs/       Delivery plan, epics, BMAD guide
Idea.MD     Full product/technical specification
```

## Design

The full UI design (all workspace screens) lives as a Claude design canvas — the visual reference
for frontend work:

**https://claude.ai/artifact/1f1xq2MaPnLgwsH34ahC9W**

It covers Projects, Overview (agent pipeline), Meetings, Intelligence, MVP (with Publish to GitHub /
Deploy to Vercel), Design, Development, QA, and Demo. Build the frontend to match it.

## Status

**Epic 0 — Foundation** in progress. See [`docs/epics/`](docs/epics) for the epic/story breakdown
and [`docs/bmad-guide.md`](docs/bmad-guide.md) for how BMAD is used in this repo.
