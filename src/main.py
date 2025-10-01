# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException

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

# Define request and response models
class AgentInput(BaseModel):
    user_input: str

class AgentResponse(BaseModel):
    processed_input: str
    action: str
    result: str
    reward: int

class MultiAgentResponse(BaseModel):
    processed_task: str
    plan: str
    result: str
    reward: int

# Initialize FastAPI
app = FastAPI(
    title="Sejal's AI Agent System",
    description="Stable API for AI agents with RL. Ready for frontend integration.",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # Redoc UI
    openapi_url="/openapi.json"  # JSON schema
)

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

# Global error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse({"detail": str(exc)}, status_code=422)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse({"detail": "Internal Server Error"}, status_code=500)

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
@app.get("/agent", response_model=AgentResponse)
def run_agent(input: str = Query(..., description="Input text for the agent", min_length=1)):
    logger.info(f"/agent called with input: {input}")
    if not input.strip():
        raise HTTPException(status_code=422, detail="Input cannot be empty")
    processed = input_handler.process_input(input)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)
    return AgentResponse(
        processed_input=processed,
        action=action,
        result=result,
        reward=reward
    )

# POST /agent endpoint
@app.post("/agent", response_model=AgentResponse)
def run_agent_post(input_data: AgentInput):
    input_text = input_data.user_input
    processed = input_handler.process_input(input_text)
    action = reasoning.plan(processed)
    result = executor.execute(action)
    reward = reward_system.calculate_reward(result)
    return AgentResponse(
        processed_input=processed,
        action=action,
        result=result,
        reward=reward
    )

# GET /multi-agent endpoint
@app.get("/multi-agent", response_model=MultiAgentResponse)
def run_multi(task: str = Query(..., description="Task for planner and executor", min_length=1)):
    processed = input_handler.process_input(task)
    plan = reasoning.plan(processed)
    result = executor.execute(plan)
    reward = reward_system.calculate_reward(result)
    return MultiAgentResponse(
        processed_task=processed,
        plan=plan,
        result=result,
        reward=reward
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))