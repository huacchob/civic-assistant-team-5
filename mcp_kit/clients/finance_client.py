"""MCP Finance Client."""

import asyncio
import os

from mcp import ClientSession, ListToolsResult, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult
from utility.sec_vars import load_secrets

# Load environment variables from .env file
load_secrets()



class FinanceClient:
    """Finance Client class."""

    def __init__(self, container_name="finance-mcp-server") -> None:
        """Initialize FinanceClient."""
        self.container_name = container_name
        self.server_params = StdioServerParameters(
            command="docker", args=["exec", "-i", container_name, "python", "server.py"]
        )
        self.session = None
        self._stdio_context = None
        self._session_context = None

    async def connect(self) -> None:
        """Establish persistent connection to Finance MCP server"""
        if self.session:
            return

        # Use proper async with pattern
        self._stdio_context = stdio_client(server=self.server_params)
        read_stream, write_stream = await self._stdio_context.__aenter__()

        self._session_context = ClientSession(
            read_stream=read_stream, write_stream=write_stream
        )
        self.session = await self._session_context.__aenter__()

        await self.session.initialize()
        print("Connected to Finance MCP server")

    async def disconnect(self) -> None:
        """Close the persistent connection"""
        if not self.session:
            return

        try:
            if self._session_context:
                await self._session_context.__aexit__(
                    exc_type=None, exc_val=None, exc_tb=None
                )
        except (Exception, asyncio.CancelledError):
            pass  # Ignore cleanup errors

        try:
            if self._stdio_context:
                await self._stdio_context.__aexit__(
                    typ=None, value=None, traceback=None
                )
        except (Exception, asyncio.CancelledError):
            pass  # Ignore cleanup errors

        self.session = None
        self._session_context = None
        self._stdio_context = None
        print("Disconnected from Finance MCP server")

    async def get_tools(self) -> list[str]:
        """Get available tools"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        tools_response: ListToolsResult = await self.session.list_tools()
        return [tool.name for tool in tools_response.tools]

    async def calculate_budget(self, income: float):
        """Calculate 30% budget from income"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        result = await self.session.call_tool(
            name="calculate_budget", arguments={"income": income}
        )
        return self._parse_budget_data(result=result, income=income)

    async def loan_qualification(self, income: float, credit_score: int):
        """Calculate maximum loan amount based on income and credit score"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        result: CallToolResult = await self.session.call_tool(
            name="loan_qualification",
            arguments={"income": income, "credit_score": credit_score},
        )
        return self._parse_loan_data(result=result)

    async def get_properties(self, loan_result: float, zip_code: str):
        """Fetch property listings from RentCast API based on max price and zip code"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
        result = await self.session.call_tool(
            name="get_properties", 
            arguments= {"loan_result": loan_result, "zip_code": zip_code}
        )
        return result  # Assuming the tool returns structured data directly    

    def _parse_budget_data(self, result, income):
        """Parse MCP result and return clean budget data"""
        if not result or not hasattr(result, "content") or not result.content:
            return result

        try:
            # The result.content is a list of TextContent objects
            if not isinstance(result.content, list) or len(result.content) == 0:
                return result

            content_text = result.content[0].text
            if not isinstance(content_text, str):
                return result

            # Extract the budget value from the text
            budget_value = float(content_text)

            # Return clean budget data with the input income
            return {"budget": budget_value, "income": income, "percentage": 0.30}
        except (ValueError, TypeError, AttributeError):
            # If parsing fails, return original result
            return result

    def _parse_loan_data(self, result):
        """Parse MCP result and return clean loan data"""
        if not result or not hasattr(result, "content") or not result.content:
            return result

        try:
            # The result.content is a list of TextContent objects
            if not isinstance(result.content, list) or len(result.content) == 0:
                return result

            content_text = result.content[0].text
            if not isinstance(content_text, str):
                return result

            # Extract the loan value from the text
            loan_value = float(content_text)

            # Return clean loan data
            return {"max_loan": loan_value}
        except (ValueError, TypeError, AttributeError):
            # If parsing fails, return original result
            return result
