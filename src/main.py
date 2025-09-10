from fastapi import FastAPI, Query
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import new modular agent modules
from src.input_handler import InputHandler
from src.reasoning import ReasoningModule
from src.executor import Executor
from src.reward import RewardSystem

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define request models
class AgentInput(BaseModel):
    user_input: str

# Initialize FastAPI
app = FastAPI(title="Sejal's AI Agent System")

# Enable CORS (important for Swagger + frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For security, replace "*" with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modular agents
input_handler = InputHandler()
reasoning = ReasoningModule()
executor = Executor()
reward_system = RewardSystem()


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "message": "FastAPI is running 🚀",
        "endpoints": ["/ping", "/agent", "/agents", "/multi-agent", "/multiagents", "/docs", "/redoc"],
        "docs": "/docs"
    }

@app.get("/ping")
def ping():
    logger.info("Ping endpoint called")
    return {"status": "ok"}


def safe_reward(value):
    """Convert reward (or any numeric) to native Python type for JSON serialization."""
    try:
        if hasattr(value, "tolist"):  # For numpy arrays
            return value.tolist()
        return int(value)  # For numpy scalars like numpy.int64
    except Exception:
        return str(value)  # fallback in case of unexpected type


@app.get("/agent")
@app.get("/agents")
def run_agent(input: str = Query(..., description="Input text for the agent")):
    logger.info(f"/agent called with input: {input}")
    
    processed = input_handler.process_input(input)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)
    
    reward = safe_reward(reward)  # convert reward to Python type
    
    return {
        "processed_input": processed,
        "action": action,
        "result": result,
        "reward": reward
    }




@app.get("/multi-agent")
@app.get("/multiagents")
def run_multi(task: str = Query(..., description="Task for planner and executor")):
    logger.info(f"/multi-agent called with task: {task}")
    
    processed = input_handler.process_input(task)
    plan = reasoning.plan(processed)
    result = executor.execute(plan)
    reward = reward_system.calculate_reward(result)
    
    reward = safe_reward(reward)
    
    return {
        "processed_task": processed,
        "plan": plan,
        "result": result,
        "reward": reward
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))  # Compatible with Render
