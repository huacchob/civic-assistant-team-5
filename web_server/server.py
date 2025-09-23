# Core imports
from contextlib import asynccontextmanager

from fastapi import FastAPI

from agents.planner_agent.graph import run_planner_agent  # Main logic entry point
from mcp_kit.tools import mcp_adapter


# Lifespan event handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mcp_adapter.connect_all()
    print(await mcp_adapter.check_running())
    print("MCP connections established")
    yield
    # Shutdown (if needed)
    pass


# FastAPI app setup
app = FastAPI(title="MAREA API", lifespan=lifespan)


# API endpoint for external access
@app.post("/analyze")
async def analyze_endpoint(income: float, credit_score: int, zip_code: str):
    try:
        user_data = {
            "income": income,
            "credit_score": credit_score,
            "zip_code": zip_code,
        }
        result = await run_planner_agent(user_data)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
