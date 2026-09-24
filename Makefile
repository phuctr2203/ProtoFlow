.PHONY: up down migrate test test-backend test-frontend

up:
	docker compose up --build

down:
	docker compose down

migrate:
	cd backend && uv run alembic upgrade head

test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest

test-frontend:
	cd frontend && npm test
