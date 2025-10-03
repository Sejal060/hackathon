# API Reference

This document describes the API endpoints, parameters, and responses for Sejal's AI Agent System. All responses are in JSON format. Use the /docs endpoint for interactive Swagger UI.

## General Information
- **Base URL**: https://ai-agent-x2iw.onrender.com
- **Authentication**: None (public API)
- **Error Responses**: 
  - 422 Unprocessable Entity: Validation errors (e.g., missing or empty input/task)
  - 500 Internal Server Error: Unexpected issues
- **Coverage**: ≥ 80%  coverage.xml or htmlcov/index.html)

## Endpoints

### GET /
- **Description**: Root endpoint to confirm the API is running.
- **Parameters**: None
- **Response** (200 OK):
{
"message": "FastAPI is running 🚀",
"docs": "/docs"
}


### GET /ping
- **Description**: Health check endpoint to verify service availability.
- **Parameters**: None
- **Response** (200 OK):
{"status": "ok"}


### GET /agent
- **Description**: Execute a single agent with a given input.
- **Parameters**:
- `input` (query, string, required, min_length=1): Input text for the agent to process.
- **Response** (200 OK): AgentResponse model
{
"processed_input": "string",
"action": "string",
"result": "string",
"reward": integer
}

- **Error Example** (422):
{
"detail": "Input cannot be empty"
}


### POST /agent
- **Description**: Execute a single agent with a JSON body input.
- **Body**: AgentInput model
{
"user_input": "string" (required)
}

- **Response** (200 OK): AgentResponse model (same as GET /agent)
{
"processed_input": "string",
"action": "string",
"result": "string",
"reward": integer
}

- **Error Example** (422): Validation error if `user_input` is missing or empty.

### GET /multi-agent
- **Description**: Execute a multi-agent task with a given task description.
- **Parameters**:
- `task` (query, string, required, min_length=1): Task for the planner and executor to process.
- **Response** (200 OK): MultiAgentResponse model
{
"processed_task": "string",
"plan": "string",
"result": "string",
"reward": integer
}

- **Error Example** (422):
{
"detail": "Task cannot be empty"
}