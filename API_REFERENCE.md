API Reference
Overview
This document outlines the FastAPI endpoints for the AI Agent System, deployed at backend.gurukul-ai.in. Access API documentation at /docs or download the OpenAPI schema at /openapi.json.
Endpoints
1. GET /agent

Description: Runs a single agent with the provided input.
Query Parameters:
input (string, required, min_length=1): The user input for the agent.


Response (200 OK):{
  "processed_input": "string",
  "action": "string",
  "result": "string",
  "reward": 1.0
}


Errors:
422: {"detail": "String should have at least 1 character"} (validation error).
500: {"detail": "Internal Server Error"} (execution failure).



2. POST /agent

Description: Runs a single agent with input and optional context.
Request Body:{
  "user_input": "string",
  "context": {"key": "value"} (optional)
}


Response (200 OK):{
  "processed_input": "string",
  "action": "string",
  "result": "string",
  "reward": 1.0
}


Errors:
422: {"detail": "Validation error"} (invalid JSON).
500: {"detail": "Internal Server Error"}.



3. GET /multi-agent

Description: Runs a multi-agent plan for the given task.
Query Parameters:
task (string, required, min_length=1): The task for the multi-agent system.


Response (200 OK):{
  "processed_task": "string",
  "plan": "string",
  "result": "string",
  "reward": 1.0
}


Errors:
422: {"detail": "String should have at least 1 character"}.
500: {"detail": "Internal Server Error"}.



4. POST /reward

Description: Calculates a reward based on action and outcome.
Request Body:{
  "action": "string",
  "outcome": "string" (optional)
}


Response (200 OK):{
  "reward_value": 1.0,
  "feedback": "string"
}


Errors:
422: {"detail": "Validation error"}.
500: {"detail": "Internal Server Error"}.



5. GET /logs

Description: Retrieves all logged actions.
Response (200 OK):[
  {
    "timestamp": "2025-10-08T13:00:00Z",
    "level": "INFO",
    "message": "string"
  }
]


Errors:
500: {"detail": "Internal Server Error"}.


