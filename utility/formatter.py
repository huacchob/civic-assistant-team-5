"""Utility functions for formatting data."""


def fmt_money(x: str) -> str:
    """Format a number as currency."""
    try:
        return f"${float(x):,.2f}"
    except Exception:
        return "N/A"
