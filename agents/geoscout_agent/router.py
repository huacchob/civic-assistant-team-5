"""Router for the GeoScout agent workflow."""
# geoscout_agent/router.py

from langgraph.graph import END
from .state import GeoScoutState


def geoscout_router(state: GeoScoutState) -> str:
    """Route to the next node based on current_step"""
    step = state.get("current_step", "")
    
    if step == "":
        return "prepare"
    elif step == "prepare":
        return "zips_and_medians"
    elif step == "zips_and_medians":
        return "filter_and_scores"
    elif step == "filter_and_scores":
        return "build_and_eval"
    elif step == "build_and_eval":
        return END
    else:
        return END

