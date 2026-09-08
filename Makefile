# MediKiosk developer commands.
.DEFAULT_GOAL := help
SHELL := /bin/bash
PY := backend/.venv/bin/python
PIP := backend/.venv/bin/pip

.PHONY: help setup db-create migrate seed reset api web dev test test-backend test-frontend build check

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Install backend and frontend dependencies
	python3 -m venv backend/.venv
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet -r backend/requirements-dev.txt
	cd frontend && npm install

db-create: ## Create the development and test databases
	createdb medikiosk || true
	createdb medikiosk_test || true

migrate: ## Apply database migrations
	cd backend && .venv/bin/alembic upgrade head

seed: ## Load the fictional demo patients
	cd backend && ../$(PY) -m app.cli seed

reset: ## Remove demo patients and OTP challenges
	cd backend && ../$(PY) -m app.cli reset

api: ## Run the API on :8000
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

web: ## Run the web app on :5173
	cd frontend && npm run dev

test: test-backend test-frontend ## Run every test

test-backend: ## Run backend tests (needs medikiosk_test)
	cd backend && .venv/bin/pytest

test-frontend: ## Run frontend tests
	cd frontend && npm run test

build: ## Production build of the web app
	cd frontend && npm run build

check: ## Typecheck the frontend
	cd frontend && npm run typecheck

docker-up: ## Run the whole stack in Docker (db + api + web on :8080)
	docker compose up --build -d
	docker compose exec -T api python -m app.cli seed

docker-down: ## Stop the Docker stack (keeps the database volume)
	docker compose down
