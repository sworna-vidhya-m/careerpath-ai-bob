# CareerPath AI MCP Server

A Model Context Protocol (MCP) server that exposes CareerPath AI analytics 
endpoints as tools for AI assistants like Bob IDE.

## Why Two Virtual Environments?

This MCP server uses Python 3.13 with its dedicated virtual environment at 
`.venv-mcp/`, while the main FastAPI application uses Python 3.9 with its 
virtual environment at the repository root's `.venv/`. The MCP SDK requires 
Python 3.10+ and uses modern syntax features, so it needs a separate, newer 
Python environment.

## Installation

The package is already installed in editable mode in the `.venv-mcp/` 
virtual environment. If you need to reinstall:

```bash
mcp/careerpath-mcp/.venv-mcp/bin/pip install -e mcp/careerpath-mcp/
```

## Running Standalone

To run the MCP server directly (for testing):

```bash
mcp/careerpath-mcp/.venv-mcp/bin/python -m careerpath_mcp
```

The server will start and communicate via stdio (standard input/output).

## Configuration

Set the `CAREERPATH_API_URL` environment variable to point to your 
CareerPath AI API instance. Default: `http://localhost:8000`

```bash
export CAREERPATH_API_URL=http://localhost:8000
mcp/careerpath-mcp/.venv-mcp/bin/python -m careerpath_mcp
```

## Registering with Bob IDE

To use this MCP server with Bob IDE:

1. Open Bob IDE Settings
2. Navigate to MCP section
3. Add a new project-level server with:
   - **Command**: `/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob/mcp/careerpath-mcp/.venv-mcp/bin/python` (use absolute path)
   - **Arguments**: `-m careerpath_mcp`
   - **Working Directory**: Repository root directory

## Available Tools

### 1. get_skill_gap

Analyzes skill gaps for an employee against their career path requirements.

**Input:**
```json
{
  "employee_id": 1
}
```

**Example Usage in Bob:**
```
Use get_skill_gap to analyze skill gaps for employee ID 1
```

### 2. get_industry_trends

Gets industry skill trends for a business unit, optionally filtered by
trend direction.

**Input:**
```json
{
  "business_unit_id": 1,
  "trend_filter": "RISING",
  "limit": 20
}
```

**Parameters:**
- `business_unit_id` (required): The ID of the business unit
- `trend_filter` (optional): Filter by trend direction - "RISING", "STABLE",
  or "DECLINING"
- `limit` (optional): Maximum number of results (default: 20)

**Example Usage in Bob:**
```
Use get_industry_trends to get rising skill trends for business unit 1
```

### 3. get_skill_heatmap

Gets organization-wide skill heatmap with proficiency distribution,
optionally filtered by business unit, skill category, or minimum importance.

**Input:**
```json
{
  "business_unit_id": 1,
  "skill_category": "TECHNICAL",
  "min_importance": 3
}
```

**Parameters:**
- `business_unit_id` (optional): Filter by business unit ID
- `skill_category` (optional): Filter by skill category - "TECHNICAL",
  "DOMAIN", or "SOFT"
- `min_importance` (optional): Filter by minimum importance level (1-5)

**Example Usage in Bob:**
```
Use get_skill_heatmap to get technical skills with importance >= 3
```

### 4. get_career_recommendations

Gets personalized career path recommendations for an employee with match
scores and skill gaps.

**Input:**
```json
{
  "employee_id": 1,
  "include_cross_bu": false,
  "max_recommendations": 5
}
```

**Parameters:**
- `employee_id` (required): The ID of the employee
- `include_cross_bu` (optional): Include cross-business-unit paths
  (default: false)
- `max_recommendations` (optional): Maximum number of recommendations
  (default: 5)

**Example Usage in Bob:**
```
Use get_career_recommendations to get career paths for employee ID 1
```

### 5. trigger_bench_learning

Auto-enrolls bench employees in learning resources targeting their career
path skill gaps. Use dry_run=true to preview without writing to DB.

**Input:**
```json
{
  "business_unit_id": 1,
  "skill_ids": [1, 2, 3],
  "max_enrollments_per_employee": 3,
  "dry_run": true
}
```

**Parameters:**
- `business_unit_id` (optional): Filter by business unit ID
- `skill_ids` (optional): Filter by specific skill IDs (array of integers)
- `max_enrollments_per_employee` (optional): Max enrollments per employee
  (1-10, default: 3)
- `dry_run` (optional): Preview without writing to DB (default: false)

**Example Usage in Bob:**
```
Use trigger_bench_learning with dry_run=true to preview bench learning
enrollments for business unit 1
```

## Testing

Run the test suite:

```bash
mcp/careerpath-mcp/.venv-mcp/bin/python -m pytest mcp/careerpath-mcp/test_server.py -v
```

## Development

The server makes HTTP calls to the FastAPI application's analytics endpoints. 
It does not import any code from the main application - all communication 
happens via HTTP.
## Bob IDE registration (one-time setup)

This repo includes `.bob/mcp.example.json` as a template. To register
this MCP server with Bob IDE on your machine:

1. Copy the example to a real config file:
```bash
   cp .bob/mcp.example.json .bob/mcp.json
```

2. Edit `.bob/mcp.json` and replace `/ABSOLUTE/PATH/TO/REPO` with the
   absolute path to your local clone of this repo.

3. Reload Bob IDE: `Cmd+Shift+P` → Developer: Reload Window

The `.bob/mcp.json` file is gitignored (it contains machine-specific paths).
