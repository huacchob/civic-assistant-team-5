"""MCP client adapter."""

from typing import Any

from .clients.finance_client import FinanceClient
from .clients.location_client import LocationClient
from .clients.supabase_client import SupabaseClient


class Adapter:
    """Adapter to manage multiple MCP clients."""

    def __init__(self) -> None:
        """Initialize Adapter with all MCP clients."""
        self.supabase = SupabaseClient()
        self.finance = FinanceClient()
        self.location = LocationClient()
        self.connected: dict[Any, Any] = {}

    async def connect_all(self) -> dict[Any, Any]:
        """Connect to all MCP services and report status"""
        # Try supabase
        try:
            await self.supabase.connect()
            self.connected["supabase"] = "connected"
        except Exception as e:
            self.connected["supabase"] = f"failed: {e}"

        # Try finance
        try:
            await self.finance.connect()
            self.connected["finance"] = "connected"
        except Exception as e:
            self.connected["finance"] = f"failed: {e}"

        # Try location
        try:
            await self.location.connect()
            self.connected["location"] = "connected"
        except Exception as e:
            self.connected["location"] = f"failed: {e}"

        return self.connected

    async def check_running(self) -> dict[Any, Any]:
        """Check which services are available"""
        return self.connected

    async def get_available_tools(self) -> dict[str, Any]:
        """Get all available tools from connected services"""
        tools = {}
        if self.connected.get("finance") == "connected":
            tools["finance"] = await self.finance.get_tools()
        if self.connected.get("supabase") == "connected":
            tools["supabase"] = await self.supabase.get_tools()
        if self.connected.get("location") == "connected":
            tools["location"] = await self.location.get_tools()
        return tools

    async def disconnect_all(self) -> dict[Any, Any]:
        """Clean shutdown of all services"""
        # Try supabase
        try:
            await self.supabase.disconnect()
            self.connected["supabase"] = "disconnected"
        except Exception:
            pass

        # Try finance
        try:
            await self.finance.disconnect()
            self.connected["finance"] = "disconnected"
        except Exception:
            pass

        # Try location
        try:
            await self.location.disconnect()
            self.connected["location"] = "disconnected"
        except Exception:
            pass

        return self.connected
