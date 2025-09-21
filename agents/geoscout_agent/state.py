"""State for the GeoScout agent workflow."""

from typing import Optional

from typing_extensions import TypedDict


class GeoScoutState(TypedDict):
    """State definition for the GeoScout Agent workflow."""

    current_step: str
    step_count: int
    error_count: int

    # User input data
    zip_code: Optional[str]

    # Transit node output
    transit_score: int
    transit_desc: str
    transit_summary: str
    lat: float
    lon: float
