"""Graph for the GeoScout agent workflow."""

"""Graph for the GeoScout Agent workflow."""

from langgraph.graph import StateGraph
from .state import GeoScoutState
from .nodes import prepare, zips_and_medians, filter_and_scores, build_and_eval


def initialize_graph() -> StateGraph:
    """Initialize the GeoScout agent graph."""
    graph = StateGraph(GeoScoutState)
    
    # Add nodes
    graph.add_node("prepare", prepare)
    graph.add_node("zips_and_medians", lambda state: zips_and_medians(state, {}))
    graph.add_node("filter_and_scores", lambda state: filter_and_scores(state, list(state["geo_scout_results"].get("medians", {}).keys())))
    graph.add_node("build_and_eval", build_and_eval)
    
    # Set up the workflow: prepare -> zips_and_medians -> filter_and_scores -> build_and_eval
    graph.set_entry_point("prepare")
    graph.add_edge("prepare", "zips_and_medians")
    graph.add_edge("zips_and_medians", "filter_and_scores")
    graph.add_edge("filter_and_scores", "build_and_eval")
    graph.set_finish_point("build_and_eval")
        
    return graph


def compile_graph():
    """Compile the graph into a runnable agent."""
    graph = initialize_graph()
    return graph.compile()


async def run_geoscout_agent(user_data):
    """Entry point to run the GeoScout agent with user data."""
    # Convert user_data to initial state
    initial_state: GeoScoutState = {
        "messages": [],
        "current_step": "prepare",
        "step_count": 0,
        "workflow_status": "in_progress",
        "location_preferences": {
            "city": user_data.get("city"),
            "budget_max": user_data.get("budget_max"),
        },
        "geo_scout_results": None,
        "error_count": 0,
        "session_id": user_data.get("session_id", "sess-1"),
    }
    
    # Create and run the graph
    agent = compile_graph()
    result = await agent.ainvoke(initial_state)
    
    return result
