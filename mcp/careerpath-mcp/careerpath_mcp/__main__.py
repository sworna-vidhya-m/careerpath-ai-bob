"""Entry point for running the MCP server."""

import asyncio

from careerpath_mcp.server import main


def run():
    """Run the MCP server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()

# Made with Bob
