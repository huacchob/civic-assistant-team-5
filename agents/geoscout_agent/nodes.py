"""Geoscout agent nodes."""

from logging import Logger
from typing import Any

from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI

from agents.geoscout_agent.prompts import (
    CommuteStructure,
    CrimeStructure,
    get_crime_score_prompt,
    get_synthesizer_prompt,
    get_transit_score_prompt,
)
from agents.geoscout_agent.state import GeoScoutState
from mcp_kit.tools import get_transit_score
from utility.logs import get_logger

logger: Logger = get_logger(name=__name__)


async def node_commute_score(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    logger.info(f"Calculating commute score for zip code: {state['zip_code']}")
    transit_score: dict[str, Any] = await get_transit_score.ainvoke(
        input={"zip_code": state["zip_code"]}
    )
    state.update(
        {
            "current_step": "commute_score",
            "step_count": 1,
            "error_count": 0,
            "transit_score": transit_score.get("transit_score", 0),
            "transit_summary": transit_score.get("summary", ""),
        }
    )
    llm = ChatOpenAI(model="gpt-4o-mini")
    structured_llm = llm.with_structured_output(
        schema=CommuteStructure,
        method="json_mode",
    )
    prompt: str = get_transit_score_prompt(
        zipcode=state["zip_code"], commute_result=transit_score
    )
    response: BaseMessage = await structured_llm.ainvoke(input=prompt)
    state.update(
        {
            "transit_summary": response.transit_summary,
        }
    )
    logger.info(f"Commute score calculation complete. Score: {state['transit_score']}")
    return state


async def node_crime_rate(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    logger.info(f"Calculating crime rate for zip code: {state['zip_code']}")
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt: str = get_crime_score_prompt(zipcode=state["zip_code"])
    structured_llm = llm.with_structured_output(
        schema=CrimeStructure,
        method="json_mode",
    )
    response: BaseMessage = await structured_llm.ainvoke(input=prompt)
    state.update(
        {
            "crime_summary": response.crime_summary,
            "crime_score": response.crime_score,
        }
    )
    logger.info(f"Crime rate calculation complete. Score: {state['crime_score']}")
    return state


async def node_synthesizer(state: GeoScoutState) -> GeoScoutState:
    """Calculate maximum loan amount based on income and credit score"""
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt: str = get_synthesizer_prompt(commute_state=state)
    response: BaseMessage = await llm.ainvoke(input=prompt)
    state.update(
        {
            "total_summary": response.content,
        }
    )
    logger.info("Synthesizer complete.")
    return state
