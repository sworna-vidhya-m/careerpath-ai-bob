"""Tests for the CareerPath MCP server."""

import pytest


def test_server_module_imports():
    """Test that the server module can be imported."""
    from careerpath_mcp import server

    assert server is not None


def test_tools_registered():
    """Test that all 5 required tools are registered."""
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

    # Verify we have exactly 5 tools
    assert len(tools) == 5, f"Expected 5 tools, got {len(tools)}"

    # Extract tool names
    tool_names = {tool.name for tool in tools}

    # Verify all 5 required tools are present
    assert "get_skill_gap" in tool_names, "get_skill_gap tool not found"
    assert (
        "get_industry_trends" in tool_names
    ), "get_industry_trends tool not found"
    assert (
        "get_skill_heatmap" in tool_names
    ), "get_skill_heatmap tool not found"
    assert (
        "get_career_recommendations" in tool_names
    ), "get_career_recommendations tool not found"
    assert (
        "trigger_bench_learning" in tool_names
    ), "trigger_bench_learning tool not found"

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

    # Verify get_skill_heatmap schema
    heatmap_tool = next(t for t in tools if t.name == "get_skill_heatmap")
    assert "business_unit_id" in heatmap_tool.inputSchema["properties"]
    assert "skill_category" in heatmap_tool.inputSchema["properties"]
    assert "min_importance" in heatmap_tool.inputSchema["properties"]
    assert len(heatmap_tool.inputSchema["required"]) == 0

    # Verify get_career_recommendations schema
    recommendations_tool = next(
        t for t in tools if t.name == "get_career_recommendations"
    )
    assert "employee_id" in recommendations_tool.inputSchema["properties"]
    assert "employee_id" in recommendations_tool.inputSchema["required"]
    assert "include_cross_bu" in recommendations_tool.inputSchema["properties"]
    assert (
        "max_recommendations" in recommendations_tool.inputSchema["properties"]
    )

    # Verify trigger_bench_learning schema
    bench_tool = next(t for t in tools if t.name == "trigger_bench_learning")
    assert "business_unit_id" in bench_tool.inputSchema["properties"]
    assert "skill_ids" in bench_tool.inputSchema["properties"]
    assert (
        "max_enrollments_per_employee"
        in bench_tool.inputSchema["properties"]
    )
    assert "dry_run" in bench_tool.inputSchema["properties"]
    assert len(bench_tool.inputSchema["required"]) == 0

# Made with Bob
