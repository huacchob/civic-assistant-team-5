"""State for the Budgeting Agent workflow."""

from typing import Any

from typing_extensions import TypedDict


class BudgetingState(TypedDict):
    """State definition for the Budgeting Agent workflow."""

    # User input data
    income: float | None
    target_home_id: int | None
    credit_score: int | None
    zip_code: str | None
    residential_units: int | None

    # Tool results
    budget_result: dict[str, Any] | None
    loan_result: dict[str, Any] | None
    price_data: dict[str, Any] | None

    # Extracted values for easy access
    monthly_budget: float | None
    max_loan: float | None

    # Usage metadata
    usage_metadata: dict[str, Any] | None
