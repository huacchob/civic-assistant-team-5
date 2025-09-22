"""MCP Finance Server."""

from typing import Any

from fastmcp import FastMCP

import httpx
import os
import utility
from utility.sec_vars import load_secrets
import pdb


# Load environment variables from .env file
load_secrets()


def get_properties(loan_result: float, zip_code: str) -> list[dict]:
    """Fetch property listings from RentCast API based on max price, zip code, and credit score"""
    
    url = f'https://api.rentcast.io/v1/listings/sale?city=Philadelphia&status=Active&priceMax=250000&limit=3'

    try:

        api_key = os.getenv("RENTCAST_API_KEY")
        if not api_key:
            raise ValueError("RENTCAST_API_KEY environment variable not set")

        headers = {
            'X-API-KEY': api_key,
            'Accept': 'application/json',
        }

        with httpx.Client() as client:
            res = client.get(url, headers=headers, timeout=10.0)
            res.raise_for_status()
            data = res.json()
            pdb.set_trace()

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
    get_properties(1300.00, '19150')
