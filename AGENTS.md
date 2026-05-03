# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Build & Test Commands

```bash
# Run app (auto-creates venv, installs deps, starts server)
./run.sh

# Run tests (requires activated venv)
source .venv/bin/activate
pytest -v

# Run single test
pytest tests/test_smoke.py::test_health_endpoint -v
```

## Local MCP Server

A local MCP (Model Context Protocol) server lives at `mcp/careerpath-mcp/`.
It exposes the analytics endpoints as tools that Bob can call directly:

- `get_skill_gap(employee_id)` — wraps GET /analytics/skill-gap/{employee_id}
- `get_industry_trends(business_unit_id, trend_filter?, limit?)` — wraps GET /analytics/industry-trends/{business_unit_id}

The MCP server uses its own Python 3.13 venv at `mcp/careerpath-mcp/.venv-mcp/`,
separate from the FastAPI app's Python 3.9 `.venv/`. They communicate over
HTTP — the MCP server requires the FastAPI app to be running on localhost:8000.

When implementing new analytics endpoints, also add corresponding MCP tools
in `mcp/careerpath-mcp/careerpath_mcp/server.py`.

## Non-Obvious Patterns

### Database & Seeding
- Database is SQLite at `data/app.db` (created on first run)
- Seeder uses `random.seed(42)` for deterministic data - DO NOT change this seed
- Seeder is idempotent via `run_if_empty()` - checks if data exists before seeding
- Tests use in-memory SQLite with `StaticPool` to persist across session (see `tests/conftest.py`)
- Tests NEVER touch `data/app.db` - they override `get_db()` dependency

### Exception Handling Pattern
- Routers must catch domain exceptions (`NotFoundError`, `DuplicateError`, etc.) from `app.exceptions`
- Use `raise_http_from_app_exception()` to translate to HTTPException with correct status codes
- Never raise HTTPException directly - use domain exceptions

### Analytics Router
- `app/routers/analytics.py` hosts five analytics endpoints (planned in PLAN.md)
- Implemented: `/analytics/health`, `/analytics/skill-gap/{employee_id}`, `/analytics/industry-trends/{business_unit_id}`
- Pending: `/analytics/skill-heatmap`, `/analytics/career-recommendations/{employee_id}`, `/analytics/trigger-bench-learning`
- New endpoints follow the exception pattern from `app/exceptions.py` and add tests in `tests/test_analytics.py`
- New endpoints should also be exposed as MCP tools (see "Local MCP Server" section)

### Code Style (from pyproject.toml)
- Line length: 100 characters (Black & Ruff configured)
- Follow existing import order in each file
- Keep functions under 50 lines where reasonable

### Testing Requirements
- New features require at least one test
- Do not delete or skip existing tests to make CI pass
- All 21 smoke tests must pass

### Security Rules
- Never log API keys, tokens, or user PII
- Validate all user input on server side
- Do not commit anything from .env or secrets/

### Workflow
- For tasks touching more than 3 files, use Plan mode before Code mode
- After code changes, run the test suite
- Reference skills in .bob/skills/ for repeatable workflows