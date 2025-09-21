"""Graph for the Planner Agent workflow."""

from typing import Any

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import run_budgeting_agent_node, run_geoscout_agent_node, synthesis_node
from .state import PlannerState


def initialize_graph() -> StateGraph[PlannerState, None, PlannerState, PlannerState]:
    """Initialize the planner agent graph with sequential agent calls."""
    graph: StateGraph[PlannerState, None, PlannerState, PlannerState] = StateGraph(
        state_schema=PlannerState,
    )

    # Add nodes for each agent
    graph.add_node(node="run_budgeting_agent", action=run_budgeting_agent_node)
    graph.add_node(node="run_geoscout_agent", action=run_geoscout_agent_node)
    graph.add_node(node="synthesis", action=synthesis_node)

    # Set up the workflow: budgeting -> synthesis
    graph.set_entry_point(key="run_budgeting_agent")
    graph.add_edge(start_key="run_budgeting_agent", end_key="run_geoscout_agent")
    graph.add_edge(start_key="run_geoscout_agent", end_key="synthesis")
    graph.set_finish_point(key="synthesis")

    return graph


def compile_graph() -> CompiledStateGraph[
    PlannerState, None, PlannerState, PlannerState
]:
    """Compile the graph into a runnable agent"""
    graph: StateGraph[PlannerState, None, PlannerState, PlannerState] = (
        initialize_graph()
    )
    return graph.compile()


async def run_planner_agent(user_data):
    """Entry point to run the planner agent with user data"""
    # Convert user_data to initial state
    initial_state: dict[str, Any] = {
        "current_step": "starting",
        "income": user_data["income"],
        "target_home_id": user_data["target_home_id"],
        "credit_score": user_data["credit_score"],
        "zip_code": user_data["zip_code"],
        "budgeting_agent_results": None,
        "geoscout_agent_results": None,
        "program_agent_results": None,
        "final_analysis": None,
    }

    # Create and run the graph
    agent: CompiledStateGraph[PlannerState, None, PlannerState, PlannerState] = (
        compile_graph()
    )
    result: dict[str, Any] | Any = await agent.ainvoke(input=initial_state)

    return result
