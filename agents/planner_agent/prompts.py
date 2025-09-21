"""Prompts for the Planner Agent workflow."""

from typing import Any


def get_comprehensive_analysis_prompt(budgeting_results: dict[Any, Any]) -> str:
    """Generate comprehensive LLM prompt for data formatting and analysis"""
    # Extract the actual values from the nested structure
    budget_value: str = (
        budgeting_results.get("budget_result", {})
        .get("budget", {})
        .get("budget", "0.0")
    )
    loan_value: str = (
        budgeting_results.get("loan_result", {})
        .get("max_loan", {})
        .get("max_loan", "0.0")
    )
    income_value = budgeting_results.get("income", "0.0")

    return f"""
    You are a financial advisor helping someone with home buying. Based on their financial data below, provide a comprehensive analysis:

    FINANCIAL DATA:
    - Income: ${income_value:,.2f}
    - Credit Score: {float(budgeting_results.get("credit_score", "0"))}
    - Monthly Budget (30% of income): ${float(budget_value):,.2f}
    - Maximum Loan Qualification: ${float(loan_value):,.2f}

    Please provide a concise analysis (max 300 words) that includes:

    1. FINANCIAL SUMMARY: Key metrics clearly
    2. READINESS: Financial readiness assessment
    3. RECOMMENDATIONS: 2-3 specific, actionable steps
    4. CONCERNS: Main issues to consider
    5. NEXT STEPS: Clear action items

    Keep it practical, actionable, and concise. Use bullet points where helpful.
    """
