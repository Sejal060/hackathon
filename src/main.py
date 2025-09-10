# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import numpy as np  # for conversion

from src.input_handler import InputHandler
from src.reasoning import ReasoningModule
from src.executor import Executor
from src.reward import RewardSystem

# Load env variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Request model
class AgentInput(BaseModel):
    user_input: str

# FastAPI app
app = FastAPI(title="Sejal's AI Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
input_handler = InputHandler()
reasoning = ReasoningModule()
executor = Executor()
reward_system = RewardSystem()

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀", "docs": "/docs"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

def convert_numpy(obj):
    """Convert NumPy types to native Python types for JSON"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

@app.get("/agent")
def run_agent(input: str = Query(..., description="Input text for the agent")):
    processed = input_handler.process_input(input)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)

    # Convert NumPy types to native Python
    result = convert_numpy(result)
    reward = convert_numpy(reward)

    return {"processed_input": processed, "action": action, "result": result, "reward": reward}

@app.post("/agent")
def run_agent_post(input_data: AgentInput):
    input_text = input_data.user_input
    processed = input_handler.process_input(input_text)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)

    # Convert NumPy types to native Python
    result = convert_numpy(result)
    reward = convert_numpy(reward)

    return {"processed_input": processed, "action": action, "result": result, "reward": reward}

@app.get("/multi-agent")
def run_multi(task: str = Query(..., description="Task for planner and executor")):
    processed = input_handler.process_input(task)
    plan = reasoning.plan(processed)
    result = executor.execute(plan)
    reward = reward_system.calculate_reward(result)

    # Convert NumPy types
    plan = convert_numpy(plan)
    result = convert_numpy(result)
    reward = convert_numpy(reward)

    return {"processed_task": processed, "plan": plan, "result": result, "reward": reward}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
