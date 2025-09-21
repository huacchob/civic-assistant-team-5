"""Main entry point for the MCP client application."""

import asyncio
import os

from fastmcp import Client

from utility.secrets import load_secrets

load_secrets()

# Dynamically build MCP URL
mcp_host = os.getenv("MCP_SERVER_NAME_NAME")
mcp_port = os.getenv("MCP_SERVER_NAME_PORT")
mcp_url = f"http://{mcp_host}:{mcp_port}/mcp"

client = Client(mcp_url)

# Import AFTER env setup to ensure LangSmith tracing applies globally
from mcp_servers.servers.server_name.client import get_mcp_data


async def main():
    """Run MCP client loop."""
    # Optionally pass MCP_URL into your client function if it accepts it
    await get_mcp_data()


if __name__ == "__main__":
    asyncio.run(main())
