# src/main.py
from fastapi import FastAPI, Query
import logging
import os
from dotenv import load_dotenv

# Import new modular agent modules
from input_handler import InputHandler
from reasoning import Reasoning
from executor import Executor
from reward import RewardSystem

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Sejal's AI Agent System")

# Initialize modular agents
input_handler = InputHandler()
reasoning = Reasoning()
executor = Executor()
reward_system = RewardSystem()

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "message": "FastAPI is running 🚀",
        "endpoints": ["/ping", "/agent", "/multi-agent", "/docs", "/redoc"],
        "docs": "http://127.0.0.1:8001/docs"
    }

@app.get("/ping")
def ping():
    logger.info("Ping endpoint called")
    return {"message": "pong"}

@app.get("/agent")
def run_agent(input: str = Query(..., description="Input text for the agent")):
    logger.info(f"/agent called with input: {input}")
    
    # Step 1: Process input
    processed = input_handler.process_input(input)
    
    # Step 2: Plan action
    action = reasoning.plan(processed)
    
    # Step 3: Execute action
    result = executor.execute(action)
    
    # Step 4: Calculate reward
    reward = reward_system.calculate_reward(result)
    
    return {"processed_input": processed, "action": action, "result": result, "reward": reward}

@app.get("/multi-agent")
def run_multi(task: str = Query(..., description="Task for planner and executor")):
    logger.info(f"/multi-agent called with task: {task}")
    
    # Reuse modular agents
    processed = input_handler.process_input(task)
    plan = reasoning.plan(processed)
    result = executor.execute(plan)
    reward = reward_system.calculate_reward(result)
    
    return {"processed_task": processed, "plan": plan, "result": result, "reward": reward}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

