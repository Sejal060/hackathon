# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Import modular agent modules
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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For security, replace "*" with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
input_handler = InputHandler()
reasoning = ReasoningModule()
executor = Executor()
reward_system = RewardSystem()

# Root endpoint
@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "FastAPI is running 🚀", "docs": "/docs"}

# Ping endpoint
@app.get("/ping")
def ping():
    return {"status": "ok"}

# GET /agent endpoint
@app.get("/agent")
def run_agent(input: str = Query(..., description="Input text for the agent")):
    logger.info(f"/agent called with input: {input}")
    
    processed = input_handler.process_input(input)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)
    
    return {
        "processed_input": processed,
        "action": action,
        "result": result,
        "reward": reward
    }

# POST /agent endpoint
@app.post("/agent")
def run_agent_post(input_data: AgentInput):
    input_text = input_data.user_input
    processed = input_handler.process_input(input_text)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)
    
    return {
        "processed_input": processed,
        "action": action,
        "result": result,
        "reward": reward
    }

# GET /multi-agent endpoint
@app.get("/multi-agent")
def run_multi(task: str = Query(..., description="Task for planner and executor")):
    processed = input_handler.process_input(task)
    plan = reasoning.plan(processed)
    result = executor.execute(plan)
    reward = reward_system.calculate_reward(result)
    
    return {
        "processed_task": processed,
        "plan": plan,
        "result": result,
        "reward": reward
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
