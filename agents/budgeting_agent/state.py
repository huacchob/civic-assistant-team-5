"""State for the Budgeting Agent workflow."""

from typing import Any, Optional

from typing_extensions import TypedDict


class BudgetingState(TypedDict):
    """State definition for the Budgeting Agent workflow."""

    # User input data
    income: Optional[float]
    target_home_id: Optional[int]
    credit_score: Optional[int]
    zip_code: Optional[str]
    motnhly_expenses: Optional[float]
    monthly_rent: Optional[float]
    total_debt: Optional[float]


    # Tool results
    budget_result: Optional[dict[str, Any]]
    property_result: Optional[dict[str, Any]]
    loan_result: Optional[dict[float, Any]]

    # Analysis and output
    analysis: Optional[dict[str, Any]]
    final_output: Optional[dict[str, Any]]
