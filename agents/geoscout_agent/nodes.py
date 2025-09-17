from __future__ import annotations

from typing import TYPE_CHECKING

from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

if TYPE_CHECKING:
    from agents.geoscout_agent.state import GeoScoutState


def init_or_resume(state: "GeoScoutState") -> "GeoScoutState":
    """Normalize step counters and mark workflow in progress."""
    state["current_step"] = state.get("current_step") or "init"
    state["step_count"] = int(state.get("step_count") or 0) + 1
    state["workflow_status"] = "in_progress"
    return state  # no external params, only state in/out


def collect_preferences(state: "GeoScoutState") -> "GeoScoutState":
    """Ensure location_preferences exist. Heuristic extraction can be added."""
    prefs = state.get("location_preferences") or {}
    # Minimal guardrails to keep node pure and deterministic here.
    # Extend with LLM-based extraction if needed.
    if "cities" not in prefs:
        prefs["cities"] = []
    if "priorities" not in prefs:
        prefs["priorities"] = []  # e.g., ["walkability", "schools", "safety"]
    if "home_type" not in prefs:
        prefs["home_type"] = None
    state["location_preferences"] = prefs
    state["current_step"] = "collect_preferences"
    state["step_count"] = state.get("step_count", 0) + 1
    return state


def scout_neighborhoods(state: "GeoScoutState") -> "GeoScoutState":
    """Produce a basic neighborhoods candidate list based on prefs."""
    prefs = state.get("location_preferences") or {}
    cities = prefs.get("cities", [])
    priorities = prefs.get("priorities", [])

    # Placeholder deterministic scoring. Replace with tools/APIs later.
    candidates = []
    for city in cities:
        candidates.append(
            {
                "city": city,
                "neighborhoods": [
                    {"name": "Central", "score": 0.75 + 0.01 * len(priorities)},
                    {"name": "North", "score": 0.70 + 0.01 * len(priorities)},
                    {"name": "East", "score": 0.68 + 0.01 * len(priorities)},
                ],
            }
        )

    state["geo_scout_results"] = {"candidates": candidates, "criteria": priorities}
    state["current_step"] = "scout_neighborhoods"
    state["step_count"] = state.get("step_count", 0) + 1
    return state


def react_summarize(state: "GeoScoutState") -> "GeoScoutState":
    """
    Final ReAct step. Uses an LLM ReAct agent to reason over results and
    produce a succinct recommendation message appended to state.messages.
    """
    results = state.get("geo_scout_results") or {}
    prefs = state.get("location_preferences") or {}

    # ReAct agent (no tools for now; add tools later as needed).
    llm = ChatOpenAI(model="gpt-4o-mini")  # pick your deployed ReAct-capable chat model
    agent = initialize_agent(
        tools=[],  # add tool instances when available
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ReAct-style
        verbose=False,
        handle_parsing_errors=True,
    )

    prompt = (
        "You are a geolocation analyst using ReAct. "
        "Reason step-by-step then give a concise, ranked recommendation.\n\n"
        f"Preferences: {prefs}\n"
        f"Candidates: {results}\n"
        "Output JSON with keys: rationale, top_neighborhoods."
    )
    try:
        conclusion = agent.run(prompt)
        # Append as an AI message-like dict to keep the state self-contained.
        state["messages"] = list(state.get("messages", [])) + [  # type: ignore
            {"type": "ai", "content": conclusion}
        ]
        state["workflow_status"] = "completed"
        state["current_step"] = "react_summarize"
    except Exception:
        state["error_count"] = int(state.get("error_count") or 0) + 1
        state["workflow_status"] = "error"
        state["current_step"] = "react_summarize_error"
    state["step_count"] = state.get("step_count", 0) + 1
    return state
