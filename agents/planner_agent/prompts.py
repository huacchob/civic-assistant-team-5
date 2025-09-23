"""Prompts for the Planner Agent workflow."""

def get_comprehensive_analysis_prompt(state: dict) -> str:
    """Generate comprehensive LLM prompt for Planner Agent synthesis (Budgeting + Program + GeoScout)."""

    # Extract results
    budgeting_results = state.get("budgeting_agent_results", {})
    program_results = state.get("program_agent_results", {}).get("filtered_programs", None)
    price_data = state.get("price_data", {})
    geoscout_results = state.get("geoscout_agent_results", {})

    # Build user profile
    prompt = f"""
You are a financial advisor helping someone with home buying. Based on their profile below, provide a comprehensive analysis:

USER PROFILE
- Income: ${state.get('income', 'N/A')}
- Credit Score: {state.get('credit_score', 'N/A')}
- Current Debt: ${state.get('current_debt', 'N/A')}
- Location Preference: {state.get('zip_code', 'N/A')} (State: {state.get('state', 'N/A')})
- Property Type: {state.get('building_class', 'N/A')} with {state.get('residential_units', 'N/A')} units
- Identity/Status: {', '.join(state.get('who_i_am', [])) if state.get('who_i_am') else 'Not specified'}
- Looking For: {', '.join(state.get('what_looking_for', [])) if state.get('what_looking_for') else 'Not specified'}

FINANCIAL CONTEXT
- Monthly Budget (30% of income): ${budgeting_results.get('monthly_budget', 'N/A')}
- Maximum Loan Qualification: ${budgeting_results.get('max_loan', 'N/A')}
- Market Data: Avg Price ${price_data.get('average_sale_price', 'N/A')} | Min ${price_data.get('min_sale_price', 'N/A')} | Max ${price_data.get('max_sale_price', 'N/A')} | Properties {price_data.get('total_properties', 'N/A')}
"""

    # Add program info
    if program_results:
        prompt += f"""

ELIGIBLE GOVERNMENT PROGRAMS
{program_results}

Note: Include ALL program details provided (name, jurisdiction, benefits, assistance type, and source link).
"""

    # Add GeoScout results
    if geoscout_results:
        items = geoscout_results.get("items", [])
        if items:
            formatted_items = "\n".join(
                [
                    f"- ZIP {i['zip']}: Median ${i['median_home_value']}, "
                    f"School Rating {i['school_rating']}, "
                    f"Transit {i['transit_score']}, "
                    f"Safety {i['safety_index']}, "
                    f"Walkability {i['walkability']}"
                    for i in items
                ]
            )
            prompt += f"""

NEIGHBORHOOD DATA (GeoScout)
{formatted_items}
"""

    # Final instructions
    prompt += """

Please provide a practical, actionable analysis (max 500 words) that includes:

1. FINANCIAL SUMMARY: Key affordability metrics
2. NEIGHBORHOOD: Interpret location/GeoScout data
3. READINESS: Financial readiness assessment
4. GOVERNMENT PROGRAMS: List ALL eligible programs with complete details
5. RECOMMENDATIONS: 2–3 specific, actionable steps
6. CONCERNS: Main issues to consider
7. NEXT STEPS: Clear action items (include program application links where possible)

Use bullet points where helpful. Keep tone professional but simple.
"""
    return prompt.strip()
