# Integration Guide for Sejal's AI Agent System

This guide explains how to integrate with the backend API for frontend engineers. Use the live URL or local setup.

## Setup
- **Local Run**: `uvicorn src.main:app --reload` (http://127.0.0.1:8000/docs for Swagger UI).
- **Live URL**: https://ai-agent-x2iw.onrender.com
- **Docs**: /docs for interactive Swagger UI, /openapi.json for raw schema.
- **Env Vars**: See RENDER_DEPLOYMENT_GUIDE.md for GROQ_API_KEY setup.

## How to Call APIs
- **Headers**: Content-Type: application/json (for POST).
- **Error Handling**: Check status codes; 422 for validation, 500 for internal errors.

## Sample Curl Commands
- GET /agent:curl "https://ai-agent-x2iw.onrender.com/agent?input=test"

- Response: AgentResponse JSON.

- POST /agent:curl -X POST "https://ai-agent-x2iw.onrender.com/agent" -H "Content-Type: application/json" -d '{"user_input": "test"}'

- Response: AgentResponse JSON.

- GET /multi-agent:curl "https://ai-agent-x2iw.onrender.com/multi-agent?task=test"

- Response: MultiAgentResponse JSON.

## Postman Collection
- Import `postman_collection.json` into Postman for pre-configured requests.

## JavaScript Example (Fetch)
fetch('https://ai-agent-x2iw.onrender.com/agent?input=test')
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));


## Troubleshooting
- 422: Check input parameters (e.g., min_length=1).
- 500: Check server logs or contact backend maintainer.