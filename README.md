
# AgentOps Studio

An AI AgentOps platform for monitoring, evaluating, and securing LLM-powered agent executions.

## Core Capabilities

- Agent execution monitoring and run history
- LLM output evaluation and quality scoring
- Token usage, cost, and latency tracking
- Execution tracing and observability
- Runtime guardrails and security checks
- Experiment tracking and comparison

## Architecture

- **Frontend:** Next.js, TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM & Migrations:** SQLAlchemy, Alembic
- **Observability:** OpenTelemetry

The application follows a modular monolith architecture.

## Local Development

### Backend

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Environment

Copy `.env.example` to `.env` and configure your local database credentials.

### Database

```bash
docker compose up -d db
```

### Run the API

```bash
uvicorn app.main:app --app-dir backend --reload
```

API documentation: http://127.0.0.1:8000/docs

### Run tests

```bash
PYTHONPATH=backend python -m pytest backend/tests -v
```

## Project Status

Under active development.
