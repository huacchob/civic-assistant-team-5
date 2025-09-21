"""Graph for the GeoScout agent workflow."""

from typing import Any

from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.geoscout_agent.nodes import (
    node_commute_score,
    node_crime_rate,
)
from agents.geoscout_agent.state import GeoScoutState


def initialize_graph() -> GeoScoutState:
    """Initialize the geo scout agent graph with model and tools."""
    graph: StateGraph[GeoScoutState] = StateGraph(state_schema=GeoScoutState)

    # Register nodes
    graph.add_node(node="node_commute_score", action=node_commute_score)
    graph.add_node(node="node_crime_rate", action=node_crime_rate)

    # Start -> init, then route
    graph.add_edge(start_key=START, end_key="node_commute_score")
    graph.add_edge(start_key="node_commute_score", end_key="node_crime_rate")

    return graph


def compile_graph() -> CompiledStateGraph[
    GeoScoutState, None, GeoScoutState, GeoScoutState
]:
    """Compile the graph into a runnable agent"""
    graph: GeoScoutState = initialize_graph()
    return graph.compile()


async def run_geoscout_agent(user_data: dict[Any, Any]) -> dict[str, Any] | Any:
    """Entry point to run the geoscout agent with user data."""
    # User input data
    initial_state = {
        "current_step": "start",
        "step_count": 0,
        "error_count": 0,
        "zip_code": user_data.get("zip_code", None),
    }

    # Create and run the graph
    agent: CompiledStateGraph[GeoScoutState, None, GeoScoutState, GeoScoutState] = (
        compile_graph()
    )
    result: dict[str, Any] | Any = await agent.ainvoke(input=initial_state)

    return result
