"""Graph for the Budgeting Agent workflow."""

from typing import Any

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import budget_calculation_node, loan_qualification_node
from .state import BudgetingState


def initialize_graph() -> StateGraph:
    """Initialize the budgeting agent graph with model and tools."""
    graph: StateGraph[BudgetingState, None, BudgetingState, BudgetingState] = (
        StateGraph(state_schema=BudgetingState)
    )

    # Add nodes
    graph.add_node(node="budget_calculation", action=budget_calculation_node)
    graph.add_node(node="loan_qualification", action=loan_qualification_node)

    # Set up the workflow: budget calculation -> loan qualification
    graph.set_entry_point(key="budget_calculation")
    graph.add_edge(start_key="budget_calculation", end_key="loan_qualification")
    graph.set_finish_point(key="loan_qualification")

    return graph


def compile_graph() -> CompiledStateGraph[
    BudgetingState, None, BudgetingState, BudgetingState
]:
    """Compile the graph into a runnable agent"""
    graph: StateGraph[BudgetingState, None, BudgetingState, BudgetingState] = (
        initialize_graph()
    )
    return graph.compile()


async def run_budgeting_agent(user_data) -> dict[str, Any] | Any:
    """Entry point to run the budgeting agent with user data"""
    # Convert user_data to initial state
    initial_state: dict[str, Any] = {
        "income": user_data["income"],
        "target_home_id": user_data["target_home_id"],
        "credit_score": user_data["credit_score"],
        "zip_code": user_data["zip_code"],
        "budget_result": None,
        "loan_result": None,
    }

    # Create and run the graph
    agent: CompiledStateGraph[BudgetingState, None, BudgetingState, BudgetingState] = (
        compile_graph()
    )
    result: dict[str, Any] | Any = await agent.ainvoke(input=initial_state)

    return result
