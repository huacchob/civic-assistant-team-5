"""Graph for the GeoScout agent workflow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agents.geoscout_agent.nodes import (
    collect_preferences,
    init_or_resume,
    react_summarize,
    scout_neighborhoods,
)
from agents.geoscout_agent.router import router
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

if TYPE_CHECKING:
    from agents.geoscout_agent.state import GeoScoutState


def build_geoscout_graph() -> CompiledStateGraph[
    GeoScoutState, None, GeoScoutState, GeoScoutState
]:
    agent_graph: StateGraph[GeoScoutState] = StateGraph(state_schema=GeoScoutState)

    # Register nodes
    agent_graph.add_node(node="init_or_resume", action=init_or_resume)
    agent_graph.add_node(node="collect_preferences", action=collect_preferences)
    agent_graph.add_node(node="scout_neighborhoods", action=scout_neighborhoods)
    agent_graph.add_node(node="react_summarize", action=react_summarize)

    # Start -> init, then route
    agent_graph.add_edge(start_key=START, end_key="init_or_resume")
    agent_graph.add_conditional_edges(
        source="init_or_resume",
        path=router,
        path_map={
            "collect_preferences": "collect_preferences",
            "scout_neighborhoods": "scout_neighborhoods",
            "react_summarize": "react_summarize",
            END: END,
        },
    )

    # After prefs -> route
    agent_graph.add_conditional_edges(
        source="collect_preferences",
        path=router,
        path_map={
            "collect_preferences": "collect_preferences",  # in case still incomplete
            "scout_neighborhoods": "scout_neighborhoods",
            "react_summarize": "react_summarize",
            END: END,
        },
    )

    # After scouting -> route
    agent_graph.add_conditional_edges(
        source="scout_neighborhoods",
        path=router,
        path_map={
            "react_summarize": "react_summarize",
            "collect_preferences": "collect_preferences",  # if prefs became invalid
            END: END,
        },
    )

    # After ReAct -> END (router handles completion/error)
    agent_graph.add_conditional_edges(
        source="react_summarize",
        path=router,
        path_map={
            END: END,
            "collect_preferences": "collect_preferences",  # rare fallback
            "scout_neighborhoods": "scout_neighborhoods",
            "react_summarize": "react_summarize",
        },
    )

    return agent_graph.compile()
