# src/main.py
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import logging
import os
import time
from dotenv import load_dotenv

# Import modular agent modules
from mcp.input_handler import InputHandler
from mcp.reasoning import ReasoningModule
from mcp.executor import Executor
from mcp.reward import RewardSystem
from mcp.reflection import reflect

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# -------------------- In-memory log store --------------------
class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

logs: List[LogEntry] = []

def log_action(message: str, level: str = "INFO"):
    """Standardized logging function."""
    logger.log(getattr(logging, level), message)
    logs.append(LogEntry(timestamp=datetime.now().isoformat(), level=level, message=message))
    # TODO: Integrate with Firebase storage

# -------------------- Request and Response Models --------------------
class AgentInput(BaseModel):
    user_input: str
    context: Optional[Dict] = None

class AgentResponse(BaseModel):
    processed_input: str
    action: str
    result: str
    reward: float

class TeamRegistrationInput(BaseModel):
    team_name: str
    members: List[str]
    email: str
    college: Optional[str] = ""
    contact_number: Optional[str] = ""

class TeamRegistrationResponse(BaseModel):
    team_id: str
    message: str

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

# -------------------- FastAPI App Initialization --------------------
def initialize_app(custom_executor=None):
    app = FastAPI(
        title="Sejal's AI Agent System",
        description="Stable API for AI agents with RL. Production-ready with OpenAPI validation.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize modules
    app.input_handler = InputHandler()
    app.reasoning = ReasoningModule()
    app.executor = custom_executor if custom_executor else Executor()
    app.reward_system = RewardSystem()

    # -------------------- Error Handlers --------------------
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        log_action(f"Validation error: {exc}", level="ERROR")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        log_action(f"Unexpected error: {exc}", level="ERROR")
        return JSONResponse({"detail": "Internal Server Error"}, status_code=500)

    # -------------------- Endpoints --------------------
    @app.get("/")
    def root():
        log_action("Root endpoint called")
        return {"message": "FastAPI is running 🚀", "docs": "/docs"}

    @app.get("/ping")
    def ping():
        log_action("Ping endpoint called")
        return {"status": "ok"}

    # GET /agent
    @app.get("/agent", response_model=AgentResponse)
    def run_agent(user_input: str = Query(..., min_length=1, description="Input text for the agent"), context: str = Query(None, description="Context for the agent")):
        start_time = time.time()
        
        log_action(f"/agent GET called with input: {user_input}")
        if not user_input.strip():
            raise HTTPException(status_code=422, detail="Input cannot be empty")
        processed = app.input_handler.process_input(user_input)
        # Convert context string to dict if provided
        context_dict = None
        if context:
            try:
                import json
                context_dict = json.loads(context)
            except:
                context_dict = {"context": context}
        action = app.reasoning.plan(processed, context_dict)
        result = app.executor.execute(action)
        reward, _ = app.reward_system.calculate_reward(result)
        
        duration_ms = (time.time() - start_time) * 1000

        # Add reflection hook
        reflect(
            module_name="agent_get",
            trace_id="N/A",  # trace_id not available in current implementation
            input_data={"user_input": user_input, "context": context},
            output_data={
                "action": action,
                "result": result,
                "reward": reward
            },
            duration_ms=duration_ms
        )
        
        return AgentResponse(processed_input=processed, action=action, result=result, reward=float(reward))

    # POST /agent
    @app.post("/agent", response_model=AgentResponse)
    def run_agent_post(input_data: AgentInput):
        start_time = time.time()
        
        # Step 1: Normalize input (using process_input as normalization)
        processed_input = app.input_handler.process_input(input_data.user_input)

        # Step 2: Reasoning / planning
        plan = app.reasoning.plan(processed_input, input_data.context)

        # Step 3: Execute the planned action
        result = app.executor.execute(plan)

        # Step 4: Calculate reward
        reward, _ = app.reward_system.calculate_reward(result)
        
        duration_ms = (time.time() - start_time) * 1000

        # Step 5: Add reflection hook
        reflect(
            module_name="agent_post",
            trace_id="N/A",  # trace_id not available in current implementation
            input_data=input_data.model_dump(),
            output_data={
                "action": plan,
                "result": result,
                "reward": reward
            },
            duration_ms=duration_ms
        )

        # Step 6: Return structured response
        return AgentResponse(
            processed_input=processed_input,
            action=plan,
            result=result,
            reward=float(reward)
        )

    # GET /multi-agent
    @app.get("/multi-agent", response_model=MultiAgentResponse)
    def run_multi(user_input: str = Query(..., min_length=1, description="Input text for the multi-agent"), context: str = Query(None, description="Context for the multi-agent")):
        start_time = time.time()
        
        log_action(f"/multi-agent GET called with input: {user_input}")
        if not user_input.strip():
            raise HTTPException(status_code=422, detail="Input cannot be empty")
        processed = app.input_handler.process_input(user_input)
        # Convert context string to dict if provided
        context_dict = None
        if context:
            try:
                import json
                context_dict = json.loads(context)
            except:
                context_dict = {"context": context}
        
        # For multi-agent processing, we'll create multiple plans and execute them
        plan = app.reasoning.plan(processed, context_dict)
        result = app.executor.execute(plan)
        reward, _ = app.reward_system.calculate_reward(result)
        
        duration_ms = (time.time() - start_time) * 1000

        # Add reflection hook
        reflect(
            module_name="multi_agent_get",
            trace_id="N/A",  # trace_id not available in current implementation
            input_data={"user_input": user_input, "context": context},
            output_data={
                "plan": plan,
                "result": result,
                "reward": reward
            },
            duration_ms=duration_ms
        )
        
        return MultiAgentResponse(processed_task=processed, plan=plan, result=result, reward=float(reward))

    # POST /reward
    @app.post("/reward", response_model=RewardResponse)
    def calculate_reward_endpoint(input_data: RewardInput):
        start_time = time.time()
        
        log_action(f"/reward POST called with action: {input_data.action}")
        try:
            reward_value, feedback = app.reward_system.calculate_reward(input_data.action, input_data.outcome)
            
            duration_ms = (time.time() - start_time) * 1000

            # Add reflection hook
            reflect(
                module_name="reward_post",
                trace_id="N/A",  # trace_id not available in current implementation
                input_data=input_data.model_dump(),
                output_data={
                    "reward_value": reward_value,
                    "feedback": feedback
                },
                duration_ms=duration_ms
            )
            
            return RewardResponse(reward_value=float(reward_value), feedback=feedback)
        except Exception as e:
            log_action(f"Error in /reward: {str(e)}", level="ERROR")
            raise HTTPException(status_code=500, detail=str(e))

    # GET /logs
    @app.get("/logs", response_model=List[LogEntry])
    def get_logs():
        log_action("Logs endpoint called")
        return logs

    # POST /register
    @app.post("/register", response_model=TeamRegistrationResponse)
    def register_team(team_data: TeamRegistrationInput):
        """Register a new team for the hackathon"""
        try:
            # Import data manager
            import sys
            import os
            # Get the absolute path to the project root
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from data_manager import DataManager
            data_manager = DataManager()
            
            # Register the team
            team_id = data_manager.register_team(
                team_name=team_data.team_name,
                members=team_data.members,
                email=team_data.email,
                college=team_data.college,
                contact_number=team_data.contact_number
            )
            
            log_action(f"Team '{team_data.team_name}' registered with ID: {team_id}")
            
            return TeamRegistrationResponse(
                team_id=team_id,
                message=f"Team '{team_data.team_name}' successfully registered"
            )
        except Exception as e:
            log_action(f"Error registering team: {str(e)}", level="ERROR")
            raise HTTPException(status_code=500, detail=str(e))

    return app

# -------------------- App Instance --------------------
app = initialize_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8002)))
