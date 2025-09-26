"""State for the Program Agent workflow."""

from typing import Any

from typing_extensions import TypedDict


class ProgramAgentState(TypedDict):
    """State definition for the Program Agent workflow."""

    # User input data (for RAG and filtering)
    who_i_am: list[str] | None
    state: str | None
    what_looking_for: list[str] | None
    income: float | None
    credit_score: int | None
    zip_code: str | None
    building_class: str | None
    current_debt: float | None
    residential_units: int | None

    # RAG results
    program_matcher_results: list[dict[str, Any]] | None  # Original RAG results (list)
    programs_text: str | None  # Original programs formatted as string
    filtered_programs: str | None  # LLM filtered response as string

    # Workflow control
    usage_metadata: dict[str, Any] | None
