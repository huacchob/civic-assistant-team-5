"""FastAPI for the MAREA project."""

from logging import Logger
from typing import Any

from fastapi import FastAPI

from agents.planner_agent.graph import run_planner_agent
from mcp_kit.tools import mcp_adapter
from utility.logs import get_logger

logger: Logger = get_logger(name=__name__)

app = FastAPI(title="MAREA API")


# Initialize MCP connections on startup
@app.on_event(event_type="startup")
async def startup() -> None:
    """Connect to all MCPs on startup."""
    await mcp_adapter.connect_all()
    logger.info(await mcp_adapter.check_running())
    logger.info("MCP connections established")


@app.post(path="/analyze")
async def analyze_endpoint(
    income: float, target_home_id: int, credit_score: int, zip_code: str
) -> dict[str, Any]:
    try:
        user_data: dict[str, Any] = {
            "income": income,
            "target_home_id": target_home_id,
            "credit_score": credit_score,
            "zip_code": zip_code,
        }
        result: dict[str, Any] | Any = await run_planner_agent(user_data=user_data)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
