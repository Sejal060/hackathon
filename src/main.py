from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .schemas.response import APIResponse

# Import modular agent modules
from src.input_handler import InputHandler
from src.reasoning import ReasoningModule
from src.executor import Executor
from src.reward import RewardSystem

# Import database module
from .database import connect_to_db_with_retry, close_db

# Load environment variables
load_dotenv()

# Validate environment variables
ENV = os.getenv("ENV", "development")
MONGODB_URI = os.getenv("MONGODB_URI")
BUCKET_DB_NAME = os.getenv("BUCKET_DB_NAME", "blackholeinifverse60_db_user")

if ENV == "production":
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI is required in production mode")
    if not BUCKET_DB_NAME:
        raise RuntimeError("BUCKET_DB_NAME is required in production mode")
else:
    if not MONGODB_URI:
        logger.warning("MONGODB_URI not set, will start in degraded mode")
    if not BUCKET_DB_NAME:
        logger.warning("BUCKET_DB_NAME not set, using default")

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

# Initialize modules
input_handler = InputHandler()
reasoning = ReasoningModule()
executor = Executor()
reward_system = RewardSystem()

# Define OpenAPI tags
tags_metadata = [
    {
        "name": "agent",
        "description": "Agent operations for processing inputs and generating actions",
    },
    {
        "name": "admin",
        "description": "Administrative operations including rewards, logs and registration",
    },
    {
        "name": "system",
        "description": "System health and monitoring endpoints",
    },
]

# Initialize FastAPI with updated metadata
app = FastAPI(
    title="HackaVerse API",
    description="Hackathon engine — agent /reward /logs",
    version="v3.0",
    contact={"name": "Sejal & Team", "email": "youremail@example.com"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata
)

@app.on_event("startup")
async def startup_event():
    # Add startup delay to ensure MongoDB is ready
    time.sleep(2)
    # Connect to database with retry logic
    connect_to_db_with_retry(retries=5, delay=2)

@app.on_event("shutdown")
async def shutdown_event():
    close_db()

# Temporary CORS unlock for frontend integration verification
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TEMPORARY UNLOCK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security middleware
from .middleware import SecurityMiddleware
app.add_middleware(SecurityMiddleware)

# Include routers
from .routes.agent import router as agent_router
from .routes.admin import router as admin_router
from .routes.system import router as system_router
from .routes.judge import router as judge_router
from .routes.workflows import router as workflows_router
from .routes.langgraph_routes import router as langgraph_router
from .routes.mcp import router as mcp_router

app.include_router(agent_router)
app.include_router(admin_router)
app.include_router(system_router, prefix="/system")
app.include_router(judge_router)
app.include_router(workflows_router)
app.include_router(langgraph_router)
app.include_router(mcp_router)

# Register error handlers
from .middleware_handlers.error_handler import api_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, api_exception_handler)

# Root endpoint
@app.get("/", summary="Root endpoint")
def root():
    log_action("Root endpoint called")
    return APIResponse(
        success=True,
        message="FastAPI is running 🚀",
        data={"docs": "/docs"}
    )

# Ping endpoint
@app.get("/ping", summary="Basic health check")
def ping():
    log_action("Ping endpoint called")
    return APIResponse(
        success=True,
        message="Service is alive",
        data=None
    )

# Endpoint definitions have been moved to the new route modules
# See src/routes/agent.py, src/routes/admin.py, and src/routes/system.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))