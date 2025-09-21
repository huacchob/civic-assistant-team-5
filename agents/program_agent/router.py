"""Router for program agent tasks."""

from .nodes import fetch_government_programs
from .state import ProgramMatcherState


async def route_program_agent(state: ProgramMatcherState) -> ProgramMatcherState:
    """Router for program agent tasks."""
    return await fetch_government_programs(state=state)
