# Here we use the OpenAI model, ask about programs, and filter based on the user profile.
from typing import Any

from langchain_openai import ChatOpenAI

from agents.program_agent.prompts import FUNDING_PROGRAM_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def fetch_government_programs(state) -> dict[str, list[dict[str, str]]]:
    """Fetch government programs node."""
    profile: Any = state.get("user_profile", {})
    query = f"Find homebuyer programs for profile: {profile}"

    # Call LLM (you can keep it async if you want actual LLM responses)
    _ = await llm.ainvoke(input=FUNDING_PROGRAM_PROMPT.format(query=query))

    # --- MOCKED structured programs (replace with parsing of LLM response) ---
    results: list[dict[str, str]] = [
        {
            "program_name": "FHA Loan",
            "eligibility": "Credit score ≥ 580, income limits apply",
            "benefits": "Low down payment (3.5%)",
            "source": "https://www.hud.gov/program_offices/housing/fhahistory",
        },
        {
            "program_name": "USDA Rural Development Loan",
            "eligibility": "Income ≤ 115% of area median, rural property",
            "benefits": "Zero down payment, lower interest rates",
            "source": "https://www.rd.usda.gov/programs-services/single-family-housing-guaranteed-loan-program",
        },
        {
            "program_name": "VA Home Loan",
            "eligibility": "Military service required",
            "benefits": "No down payment, no PMI",
            "source": "https://www.benefits.va.gov/homeloans/",
        },
    ]

    # --- Filter based on user profile ---
    filtered: list[dict[str, str]] = []
    for prog in results:
        if prog["program_name"] == "FHA Loan" and profile.get("credit_score", 0) < 580:
            continue
        if (
            prog["program_name"] == "USDA Rural Development Loan"
            and profile.get("income", 0) > 60000
        ):
            continue
        if prog["program_name"] == "VA Home Loan" and not profile.get(
            "military", False
        ):
            continue
        filtered.append(prog)

    return {"program_matcher_results": filtered}
