"""Nodes for the Budgeting Agent workflow."""

from typing import Any

from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI

from .prompts import get_budget_calculation_prompt
from .state import BudgetingState


async def budget_calculation_node(state: BudgetingState) -> BudgetingState:
    """Calculate 30% budget from user income"""
    from mcp_kit.tools import calculate_budget

    # Call the tool directly to get the budget (async)
    budget_result: Any = await calculate_budget.ainvoke(
        input={"income": state["income"]}
    )
    print(f"Budget calculation result: {budget_result}")

    model = ChatOpenAI(model="gpt-4o-mini")

    # Use the existing prompt from prompts.py with the budget result
    prompt: str = get_budget_calculation_prompt(
        income=state["income"], budget_result=budget_result
    )

    response: BaseMessage = await model.ainvoke(input=prompt)
    print(f"Model response: {response.content}")

    # Store both the tool result and the model's explanation
    state["budget_result"] = {
        "tool_result": budget_result,
        "explanation": response.content,
    }

    return state


async def loan_qualification_node(state: BudgetingState) -> BudgetingState:
    """Calculate maximum loan amount based on income and credit score"""
    from mcp_kit.tools import loan_qualification

    # Call the loan qualification tool
    loan_result: Any = await loan_qualification.ainvoke(
        input={"income": state["income"], "credit_score": state["credit_score"]}
    )
    print(f"Loan qualification result: {loan_result}")

    # Store just the raw tool result
    state["loan_result"] = loan_result

    return state


async def property_listing_node(state: BudgetingState) -> BudgetingState:
    """Fetch property listings based on max loan amount and zip code"""
    from mcp_kit.tools import get_properties

    # Call the get_properties tool
    properties_result: Any = await get_properties.ainvoke(
        input={"loan_result": state["loan_result"]['max_loan']['max_loan'], "zip_code": state["zip_code"]}
    )
    print(f"Property listings result: {properties_result}")

    # Store the property listings
    state["property_listings"] = properties_result

    return state
