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
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_skill_gap":
        return await handle_get_skill_gap(arguments)
    elif name == "get_industry_trends":
        return await handle_get_industry_trends(arguments)
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
