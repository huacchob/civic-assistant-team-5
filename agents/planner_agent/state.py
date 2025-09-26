"""State for the Planner Agent workflow."""

from typing import Any

from typing_extensions import TypedDict


class PlannerState(TypedDict):
    # User input data (from frontend)
    income: float | None
    state: str | None  # State selection
    credit_score: int | None
    zip_code: str | None
    residential_units: int | None
    current_debt: float | None
    building_class: str | None
    who_i_am: list | None  # User identity/status selections
    what_looking_for: list | None  # What they're looking for selections s

    # Program state
    program_agent_results: dict[str, Any] | None

    # Geoscout agent
    geoscout_agent_results: dict[str, Any] | None

    # Budgeting agent
    price_data: dict[str, Any] | None  # Market pricing data (avg, min, max, etc.)
    property_data: dict[str, Any] | None  # Results from home_id query
    monthly_budget: float | None
    max_loan: float | None
    budgeting_agent_results: dict[str, Any] | None

    # Planner-specific outputs
    final_analysis: str | None  # Comprehensive synthesis

    # Usage metadata
    usage_metadata: dict[str, Any] | None
