"""Router for the GeoScout agent workflow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from langgraph.graph import END

if TYPE_CHECKING:
    from agents.geoscout_agent.state import GeoScoutState


def router(state: GeoScoutState) -> str:
    """
    Dynamically pick the next node.
    - If missing prefs -> collect_preferences
    - If have prefs but no results -> scout_neighborhoods
    - If have results -> react_summarize
    - If completed or error -> END
    """
    status = state.get("workflow_status")
    if status in ("completed", "error"):
        return END

    prefs = state.get("location_preferences") or {}
    results = state.get("geo_scout_results")

    if not prefs or not isinstance(prefs, dict) or (not prefs.get("cities")):
        return "collect_preferences"

    if not results:
        return "scout_neighborhoods"

    return "react_summarize"
