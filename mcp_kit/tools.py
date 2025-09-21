"""Agent MCP tool registry."""

from typing import Any

from langchain_core.tools import tool

from mcp_kit.adapter import Adapter

mcp_adapter = Adapter()


@tool
async def calculate_budget(income: float) -> dict[str, Any]:
    """Calculate 30% budget from income using Finance MCP"""
    result: Any = await mcp_adapter.finance.calculate_budget(income=income)
    return {"budget": result}


@tool
async def loan_qualification(income: float, credit_score: int) -> dict[str, Any]:
    """Calculate maximum loan amount based on income and credit score using Finance MCP"""
    result: Any = await mcp_adapter.finance.loan_qualification(
        income=income, credit_score=credit_score
    )
    return {"max_loan": result}


@tool
async def query_home_by_id(home_id: int) -> dict[str, Any]:
    """Query NYC property sales data using Supabase MCP by HOME_ID"""
    result: Any = await mcp_adapter.supabase.query_home_by_id(home_id=home_id)
    return {"property": result}


@tool
async def get_transit_score(zip_code: str) -> dict[str, Any]:
    """Get transit score and summary for a specific location using Location MCP"""
    result: Any = await mcp_adapter.location.get_transit_score(zip_code=zip_code)
    return {"transit_score": result}
