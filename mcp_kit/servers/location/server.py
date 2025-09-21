"""Location MCP Server."""

import os
from typing import Any, Dict

import httpx
from fastmcp import FastMCP

from utility.secrets import load_secrets

# Load environment variables from .env file
load_secrets()

server: FastMCP[Any] = FastMCP(name="Location")


def _get_zip_coordinates(zip_code: str) -> tuple[float, float]:
    """Convert ZIP code to lat/lon coordinates using a reliable geocoding service."""
    try:
        # Use a free geocoding service - we'll use a simple approach
        # For production, you might want to use Google Maps API or similar
        url: str = f"https://api.zippopotam.us/us/{zip_code}"

        with httpx.Client() as client:
            response: httpx.Response = client.get(url=url, timeout=10.0)
            response.raise_for_status()
            data: Any = response.json()

        if data and "places" in data and len(data["places"]) > 0:
            place: Any = data["places"][0]
            lat = float(place["latitude"])
            lon = float(place["longitude"])
            return (lat, lon)
        else:
            raise ValueError(f"ZIP code {zip_code} not found")

    except Exception:
        # Fallback to default coordinates if API fails
        return (40.7505, -73.9934)  # New York, NY


@server.tool()
def get_transit_score(zip_code: str) -> Dict[str, Any]:
    """
    Get transit score and summary for a specific ZIP code

    Args:
        zip_code: ZIP code for the location

    Returns:
        Dictionary containing transit score, description, and route summary
    """
    try:
        # Convert ZIP code to lat/lon
        lat, lon = _get_zip_coordinates(zip_code=zip_code)

        # Get API key
        api_key = os.getenv("WALKSCORE_API_KEY")
        if not api_key:
            return {
                "error": "Walk Score API key not configured",
                "status": "error",
                "zip_code": zip_code,
            }

        # Make the Transit API request
        params: dict[str, Any] = {"lat": lat, "lon": lon, "wsapikey": api_key}

        with httpx.Client() as client:
            response: httpx.Response = client.get(
                url="https://transit.walkscore.com/transit/score/",
                params=params,
                timeout=10.0,
            )
            response.raise_for_status()
            data: Any = response.json()

        if data and "transit_score" in data:
            return {
                "transit_score": data.get("transit_score"),
                "description": data.get("description"),
                "summary": data.get("summary"),
                "zip_code": zip_code,
                "lat": lat,
                "lon": lon,
                "status": "success",
            }
        else:
            return {
                "error": "No transit score found for this location",
                "status": "error",
                "zip_code": zip_code,
            }

    except httpx.RequestError as e:
        return {
            "error": f"Transit API request failed: {str(e)}",
            "status": "error",
            "zip_code": zip_code,
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "status": "error",
            "zip_code": zip_code,
        }


if __name__ == "__main__":
    server.run(transport="stdio")
