"""State definitions for the Program Agent workflow."""

from typing import Any, Literal

from langchain_core.messages import BaseMessage
from typing_extensions import Annotated, TypedDict


class ProgramMatcherState(TypedDict):
    """State definition for the Program Matcher workflow."""

    messages: Annotated[list[BaseMessage], "add_messages"]
    current_step: str
    step_count: int
    workflow_status: Literal["in_progress", "completed", "error"]
    user_profile: dict[str, Any]
    program_matcher_results: list[dict[str, Any]]  # <-- make sure it's a list
    error_count: int
    session_id: str
