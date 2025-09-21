"""Geoscout agent nodes."""

from typing import Any

from agents.geoscout_agent.state import GeoScoutState
from mcp_kit.tools import get_transit_score


async def node_commute_score(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    transit_result: dict[str, Any] = await get_transit_score.ainvoke(
        input={"zip_code": state["zip_code"]}
    )
    state.update(
        {
            "current_step": "commute_score",
            "step_count": 1,
            "error_count": 0,
            "transit_score": transit_result.get("transit_score", 0),
            "transit_desc": transit_result.get("description", ""),
            "transit_summary": transit_result.get("summary", ""),
            "lat": transit_result.get("lat", 0.0),
            "lon": transit_result.get("lon", 0.0),
        }
    )
    return state


async def node_crime_rate(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    print("   Calling crime rate tool...")
    # from mcp_kit.tools import loan_qualification

    # # Call the loan qualification tool
    # loan_result = await loan_qualification.ainvoke(
    #     {"income": state["income"], "credit_score": state["credit_score"]}
    # )
    # print(f"Loan qualification result: {loan_result}")

    # # Store just the raw tool result
    # state["loan_result"] = loan_result

    # return state
