"""Tests for the CareerPath MCP server."""

import pytest


def test_server_module_imports():
    """Test that the server module can be imported."""
    from careerpath_mcp import server

    assert server is not None


def test_tools_registered():
    """Test that both required tools are registered."""
    import asyncio

    from mcp.types import ListToolsRequest
    from careerpath_mcp.server import app

    # Get the list_tools handler from request_handlers
    list_tools_handler = app.request_handlers.get(ListToolsRequest)
    assert list_tools_handler is not None, "No list_tools handler registered"

    # Call the handler to get tools (it's async, so we need to run it)
    request = ListToolsRequest()
    result = asyncio.run(list_tools_handler(request))

    # Extract tools from the result (result.root contains ListToolsResult)
    tools = result.root.tools

    # Verify we have exactly 2 tools
    assert len(tools) == 2, f"Expected 2 tools, got {len(tools)}"

    # Extract tool names
    tool_names = {tool.name for tool in tools}

    # Verify both required tools are present
    assert "get_skill_gap" in tool_names, "get_skill_gap tool not found"
    assert (
        "get_industry_trends" in tool_names
    ), "get_industry_trends tool not found"

    # Verify get_skill_gap schema
    skill_gap_tool = next(t for t in tools if t.name == "get_skill_gap")
    assert "employee_id" in skill_gap_tool.inputSchema["properties"]
    assert "employee_id" in skill_gap_tool.inputSchema["required"]

    # Verify get_industry_trends schema
    trends_tool = next(t for t in tools if t.name == "get_industry_trends")
    assert "business_unit_id" in trends_tool.inputSchema["properties"]
    assert "business_unit_id" in trends_tool.inputSchema["required"]
    assert "trend_filter" in trends_tool.inputSchema["properties"]
    assert "limit" in trends_tool.inputSchema["properties"]

# Made with Bob
