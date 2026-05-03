"""MCP server for CareerPath AI analytics."""

import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.types import TextContent, Tool


# Read API base URL from environment, default to localhost
API_BASE_URL = os.getenv("CAREERPATH_API_URL", "http://localhost:8000")

# Initialize the MCP server
app = Server("careerpath-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_skill_gap",
            description=(
                "Analyze skill gaps for an employee against their career "
                "path requirements"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The ID of the employee to analyze",
                    }
                },
                "required": ["employee_id"],
            },
        ),
        Tool(
            name="get_industry_trends",
            description=(
                "Get industry skill trends for a business unit, optionally "
                "filtered by trend direction"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "business_unit_id": {
                        "type": "integer",
                        "description": "The ID of the business unit",
                    },
                    "trend_filter": {
                        "type": "string",
                        "enum": ["RISING", "STABLE", "DECLINING"],
                        "description": "Filter by trend direction",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 20,
                    },
                },
                "required": ["business_unit_id"],
            },
        ),
        Tool(
            name="get_skill_heatmap",
            description=(
                "Get organization-wide skill heatmap with proficiency "
                "distribution, optionally filtered by business unit, skill "
                "category, or minimum importance"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "business_unit_id": {
                        "type": "integer",
                        "description": "Filter by business unit ID",
                    },
                    "skill_category": {
                        "type": "string",
                        "enum": ["TECHNICAL", "DOMAIN", "SOFT"],
                        "description": "Filter by skill category",
                    },
                    "min_importance": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Filter by minimum importance level",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_career_recommendations",
            description=(
                "Get personalized career path recommendations for an "
                "employee with match scores and skill gaps"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The ID of the employee",
                    },
                    "include_cross_bu": {
                        "type": "boolean",
                        "description": "Include cross-business-unit paths",
                        "default": False,
                    },
                    "max_recommendations": {
                        "type": "integer",
                        "description": "Maximum number of recommendations",
                        "default": 5,
                    },
                },
                "required": ["employee_id"],
            },
        ),
        Tool(
            name="trigger_bench_learning",
            description=(
                "Auto-enroll bench employees in learning resources "
                "targeting their career path skill gaps. Use dry_run=true "
                "to preview without writing to DB."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "business_unit_id": {
                        "type": "integer",
                        "description": "Filter by business unit ID",
                    },
                    "skill_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Filter by specific skill IDs",
                    },
                    "max_enrollments_per_employee": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "description": "Max enrollments per employee",
                        "default": 3,
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "Preview without writing to DB",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_skill_gap":
        return await handle_get_skill_gap(arguments)
    elif name == "get_industry_trends":
        return await handle_get_industry_trends(arguments)
    elif name == "get_skill_heatmap":
        return await handle_get_skill_heatmap(arguments)
    elif name == "get_career_recommendations":
        return await handle_get_career_recommendations(arguments)
    elif name == "trigger_bench_learning":
        return await handle_trigger_bench_learning(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_get_skill_gap(arguments: dict) -> list[TextContent]:
    """Handle get_skill_gap tool call."""
    employee_id = arguments["employee_id"]
    url = f"{API_BASE_URL}/analytics/skill-gap/{employee_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [
                TextContent(
                    type="text",
                    text=str(data),
                )
            ]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_data = e.response.json()
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {error_data.get('detail', 'Not found')}",
                    )
                ]
            raise


async def handle_get_industry_trends(arguments: dict) -> list[TextContent]:
    """Handle get_industry_trends tool call."""
    business_unit_id = arguments["business_unit_id"]
    url = f"{API_BASE_URL}/analytics/industry-trends/{business_unit_id}"

    # Build query parameters
    params = {}
    if "trend_filter" in arguments:
        params["trend_filter"] = arguments["trend_filter"]
    if "limit" in arguments:
        params["limit"] = arguments["limit"]
    else:
        params["limit"] = 20

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [
                TextContent(
                    type="text",
                    text=str(data),
                )
            ]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_data = e.response.json()
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {error_data.get('detail', 'Not found')}",
                    )
                ]
            raise


async def handle_get_skill_heatmap(arguments: dict) -> list[TextContent]:
    """Handle get_skill_heatmap tool call."""
    url = f"{API_BASE_URL}/analytics/skill-heatmap"

    # Build query parameters
    params = {}
    if "business_unit_id" in arguments:
        params["business_unit_id"] = arguments["business_unit_id"]
    if "skill_category" in arguments:
        params["skill_category"] = arguments["skill_category"]
    if "min_importance" in arguments:
        params["min_importance"] = arguments["min_importance"]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [
                TextContent(
                    type="text",
                    text=str(data),
                )
            ]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_data = e.response.json()
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {error_data.get('detail', 'Not found')}",
                    )
                ]
            raise


async def handle_get_career_recommendations(
    arguments: dict
) -> list[TextContent]:
    """Handle get_career_recommendations tool call."""
    employee_id = arguments["employee_id"]
    url = f"{API_BASE_URL}/analytics/career-recommendations/{employee_id}"

    # Build query parameters
    params = {}
    if "include_cross_bu" in arguments:
        params["include_cross_bu"] = arguments["include_cross_bu"]
    else:
        params["include_cross_bu"] = False
    if "max_recommendations" in arguments:
        params["max_recommendations"] = arguments["max_recommendations"]
    else:
        params["max_recommendations"] = 5

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [
                TextContent(
                    type="text",
                    text=str(data),
                )
            ]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_data = e.response.json()
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {error_data.get('detail', 'Not found')}",
                    )
                ]
            raise


async def handle_trigger_bench_learning(arguments: dict) -> list[TextContent]:
    """Handle trigger_bench_learning tool call."""
    url = f"{API_BASE_URL}/analytics/trigger-bench-learning"

    # Build request body
    body = {}
    if "business_unit_id" in arguments:
        body["business_unit_id"] = arguments["business_unit_id"]
    if "skill_ids" in arguments:
        body["skill_ids"] = arguments["skill_ids"]
    if "max_enrollments_per_employee" in arguments:
        body["max_enrollments_per_employee"] = arguments[
            "max_enrollments_per_employee"
        ]
    else:
        body["max_enrollments_per_employee"] = 3
    if "dry_run" in arguments:
        body["dry_run"] = arguments["dry_run"]
    else:
        body["dry_run"] = False

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=body)
            response.raise_for_status()
            data = response.json()
            return [
                TextContent(
                    type="text",
                    text=str(data),
                )
            ]
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (404, 422):
                error_data = e.response.json()
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {error_data.get('detail', 'Error')}",
                    )
                ]
            raise


async def main():
    """Run the MCP server using stdio transport."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )

# Made with Bob
