# src/main.py
from fastapi import FastAPI, Query
from .agent import BasicAgent
from .multi_agent import PlannerAgent, ExecutorAgent, Environment
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Sejal's AI Agent System")

# Initialize agents with API key
api_key = os.getenv("GROQ_API_KEY", "")
agent = BasicAgent(api_key=api_key)
planner = PlannerAgent(api_key=api_key)
executor = ExecutorAgent(api_key=api_key)
env = Environment()

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
    return agent.process_input(input)

@app.get("/multi-agent")
def run_multi(task: str = Query(..., description="Task for planner and executor")):
    logger.info(f"/multi-agent called with task: {task}")
    plan = planner.propose_plan(task)
    result = executor.execute_plan(plan)
    reward = env.give_reward(result)
    return {"plan": plan, "result": result, "reward": reward}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # change port if needed
