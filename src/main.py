from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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

# In-memory log store (temporary; to be replaced by Nipun's Firebase storage layer)
class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

logs: List[LogEntry] = []

def log_action(message: str, level: str = "INFO"):
    """Standardized logging function."""
    logger.log(getattr(logging, level), message)
    logs.append(LogEntry(timestamp=datetime.now().isoformat(), level=level, message=message))
    # TODO: Integrate with firebase-admin to persist logs (Nipun's storage layer)

# Define request and response models
class AgentInput(BaseModel):
    user_input: str
    context: Optional[Dict] = None

class AgentResponse(BaseModel):
    processed_input: str
    action: str
    result: str
    reward: float

class RewardInput(BaseModel):
    action: str
    outcome: Optional[str] = None

class RewardResponse(BaseModel):
    reward_value: float
    feedback: str

class MultiAgentInput(BaseModel):
    task: str
    context: Optional[Dict] = None

class MultiAgentResponse(BaseModel):
    processed_task: str
    plan: str
    result: str
    reward: float

# Initialize FastAPI and modules
def initialize_app(custom_executor=None):
    app = FastAPI(
        title="Sejal's AI Agent System",
        description="Stable API for AI agents with RL. Ready for frontend integration.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with app.gurukul-ai.in in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize modules with optional custom executor
    app.input_handler = InputHandler()
    app.reasoning = ReasoningModule()
    app.executor = custom_executor if custom_executor else Executor()
    app.reward_system = RewardSystem()

    # Global error handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        log_action(f"Validation error: {exc}", level="ERROR")
        return JSONResponse({"detail": str(exc)}, status_code=422)

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        log_action(f"Unexpected error: {exc}", level="ERROR")
        return JSONResponse({"detail": "Internal Server Error"}, status_code=500)

    # Root endpoint
    @app.get("/")
    def root():
        log_action("Root endpoint called")
        return {"message": "FastAPI is running 🚀", "docs": "/docs"}

    # Ping endpoint
    @app.get("/ping")
    def ping():
        log_action("Ping endpoint called")
        return {"status": "ok"}

    # GET /agent endpoint
    @app.get("/agent", response_model=AgentResponse)
    def run_agent(input: str = Query(..., description="Input text for the agent", min_length=1)):
        log_action(f"/agent GET called with input: {input}")
        if not input.strip():
            raise HTTPException(status_code=422, detail="Input cannot be empty")
        processed = app.input_handler.process_input(input)
        action = app.reasoning.plan(processed)  # No context for GET
        result = app.executor.execute(action)
        reward, _ = app.reward_system.calculate_reward(result)
        return AgentResponse(
            processed_input=processed,
            action=action,
            result=result,
            reward=float(reward)
        )

    # POST /agent endpoint
    @app.post("/agent", response_model=AgentResponse)
    def run_agent_post(input_data: AgentInput):
        log_action(f"/agent POST called with input: {input_data.user_input}")
        processed = app.input_handler.process_input(input_data.user_input)
        action = app.reasoning.plan(processed, input_data.context)  # Pass context
        result = app.executor.execute(action)
        reward, _ = app.reward_system.calculate_reward(result)
        return AgentResponse(
            processed_input=processed,
            action=action,
            result=result,
            reward=float(reward)
        )

    # GET /multi-agent endpoint
    @app.get("/multi-agent", response_model=MultiAgentResponse)
    def run_multi(task: str = Query(..., description="Task for planner and executor", min_length=1)):
        log_action(f"/multi-agent called with task: {task}")
        processed = app.input_handler.process_input(task)
        plan = app.reasoning.plan(processed)  # No context for GET
        result = app.executor.execute(plan)
        reward, _ = app.reward_system.calculate_reward(result)
        return MultiAgentResponse(
            processed_task=processed,
            plan=plan,
            result=result,
            reward=float(reward)
        )

    # POST /reward endpoint
    @app.post("/reward", response_model=RewardResponse)
    def calculate_reward_endpoint(input_data: RewardInput):
        log_action(f"/reward called with action: {input_data.action}")
        try:
            reward_value, feedback = app.reward_system.calculate_reward(input_data.action, input_data.outcome)
            return RewardResponse(
                reward_value=float(reward_value),
                feedback=feedback
            )
        except Exception as e:
            log_action(f"Error in /reward: {str(e)}", level="ERROR")
            raise HTTPException(status_code=500, detail=str(e))

    # GET /logs endpoint
    @app.get("/logs", response_model=List[LogEntry])
    def get_logs():
        log_action("Logs endpoint called")
        return logs  # TODO: Replace with Firebase query in Nipun's storage layer

    return app

# Initial app instance
app = initialize_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))