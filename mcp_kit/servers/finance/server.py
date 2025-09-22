"""MCP Finance Server."""

from typing import Any

from fastmcp import FastMCP

import httpx

server: FastMCP[Any] = FastMCP(name="Finance")


@server.tool()
def calculate_budget(income: float) -> float:
    """Calculate 30% budget from income"""
    return income * 0.30


@server.tool()
def loan_qualification(income: float, credit_score: int) -> float:
    """Calculate maximum loan amount based on income and credit score"""
    if credit_score >= 750:
        multiplier = 5.0
    elif credit_score >= 700:
        multiplier = 4.5
    elif credit_score >= 650:
        multiplier = 4.0
    elif credit_score >= 580:
        multiplier = 3.5
    else:
        multiplier = 2.5

    return income * multiplier

@server.tool() # Call rentcast API to get property listings
def get_properties(loan_result: float, zip_code: str) -> list[dict]:
    """Fetch property listings from RentCast API based on max price, zip code, and credit score"""
    
    url = f'https://api.rentcast.io/v1/listings/sale?zipcode={zip_code}&status=Active&price={loan_result}&limit=3'

    try:

        api_key = os.getenv("RENTCAST_API_KEY")
        if not api_key:
            raise ValueError("RENTCAST_API_KEY environment variable not set")

        headers = {
            'x-api-key': api_key,
            'Accept': 'application/json',
        }

        with httpx.Client() as client:
            res = client.get(url, headers=headers timeout=10.0)
            res.raise_for_status()
            data = res.json()

        if data and "listings" in data:
            l = {
                '1': (data[0]['formattedAddress'],
                      data[0]['price'],
                      data[0]['daysOnMarket']),

                '2': (data[1]['formattedAddress'],
                      data[1]['price'],
                      data[1]['daysOnMarket']),

                '3': (data[2]['formattedAddress'], 
                      data[2]['price'],
                      data[2]['daysOnMarket'])                     
                
            }
            print('********Succesfully called API********')
            return l.json()
       
        else:
            raise ValueError("No listings found")
    
    except httpx.RequestError as e:
        raise ValueError(f"RentCast API request failed: {str(e)}")


if __name__ == "__main__":
    server.run(transport="stdio")
