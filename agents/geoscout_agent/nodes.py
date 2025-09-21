"""Geoscout agent nodes."""

from agents.geoscout_agent.state import GeoScoutState


async def node_commute_score(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    print("   Calling commute score tool...")
    # from mcp_kit.tools import loan_qualification

    # # Call the loan qualification tool
    # loan_result = await loan_qualification.ainvoke(
    #     {"income": state["income"], "credit_score": state["credit_score"]}
    # )
    # print(f"Loan qualification result: {loan_result}")

    # # Store just the raw tool result
    # state["loan_result"] = loan_result

    # return state


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
