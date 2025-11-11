# HackaVerse API Reference

## Overview
HackaVerse API v2.0 - Hackathon engine for agent processing, reward calculation, and logging.

## Base URL
Local: http://127.0.0.1:8001
Deployed: https://ai-agent-x2iw.onrender.com

## Authentication
No authentication required for current endpoints.

## Error Handling
The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 422: Validation Error
- 500: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## Endpoints

### Agent Endpoints

#### POST /agent/
Process agent requests and generate responses.

**Request Body:**
```json
{
  "team_id": "string",
  "prompt": "string",
  "metadata": {}
}
```

**Response:**
```json
{
  "processed_input": "string",
  "action": "string",
  "result": "string",
  "reward": 0.0,
  "core_response": {}
}
```

**Example:**
```bash
curl -X POST https://ai-agent-x2iw.onrender.com/agent/ \
  -H "Content-Type: application/json" \
  -d '{"team_id":"team_42","prompt":"How to build a REST API?","metadata":{}}'
```

### Admin Endpoints

#### POST /admin/reward
Calculate and apply rewards based on request outcomes.

**Request Body:**
```json
{
  "request_id": "string",
  "outcome": "string"
}
```

**Response:**
```json
{
  "reward_value": 0.0,
  "feedback": "string"
}
```

**Example:**
```bash
curl -X POST https://ai-agent-x2iw.onrender.com/admin/reward \
  -H "Content-Type: application/json" \
  -d '{"request_id":"req_123","outcome":"success"}'
```

#### POST /admin/logs
Relay logs to the BHIV Bucket for storage and analysis.

**Request Body:**
```json
{
  "timestamp": "string",
  "level": "string",
  "message": "string",
  "additional_data": {}
}
```

**Response:**
```json
{
  "status": "string",
  "result": "string"
}
```

**Example:**
```bash
curl -X POST https://ai-agent-x2iw.onrender.com/admin/logs \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-01-01T12:00:00Z","level":"INFO","message":"Team submitted project"}'
```

#### POST /admin/register
Register a new team for the hackathon.

**Request Body:**
```json
{
  "team_name": "string",
  "members": ["string"],
  "project_title": "string"
}
```

**Response:**
```json
{
  "message": "Team registered successfully",
  "team_id": "string"
}
```

**Example:**
```bash
curl -X POST https://ai-agent-x2iw.onrender.com/admin/register \
  -H "Content-Type: application/json" \
  -d '{"team_name":"Innovators","members":["Alice","Bob"],"project_title":"AI Assistant"}'
```

#### POST /admin/webhook/hackaverse/registration
N8N webhook endpoint for automated team registration.

**Request Body:**
```json
{
  "team_name": "string",
  "members": ["string"],
  "project_title": "string"
}
```

**Response:**
```json
{
  "status": "registered",
  "team_id": "string"
}
```

**Example:**
```bash
curl -X POST https://ai-agent-x2iw.onrender.com/admin/webhook/hackaverse/registration \
  -H "Content-Type: application/json" \
  -d '{"team_name":"TechStars","members":["Charlie","Diana"],"project_title":"Blockchain Voting"}'
```

### System Endpoints

#### GET /system/health
Check system health and get operational status.

**Response:**
```json
{
  "status": "healthy",
  "version": "v2.0",
  "timestamp": "string",
  "platform": "string",
  "python_version": "string"
}
```

**Example:**
```bash
curl https://ai-agent-x2iw.onrender.com/system/health
```

#### GET /ping
Basic health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl https://ai-agent-x2iw.onrender.com/ping
```

#### GET /
Root endpoint with API information.

**Response:**
```json
{
  "message": "FastAPI is running 🚀",
  "docs": "/docs"
}
```

**Example:**
```bash
curl https://ai-agent-x2iw.onrender.com/
```

## Data Models

### AgentRequest
```json
{
  "team_id": "string",
  "prompt": "string",
  "metadata": {}
}
```

### AgentResponse
```json
{
  "processed_input": "string",
  "action": "string",
  "result": "string",
  "reward": 0.0,
  "core_response": {}
}
```

### TeamRegistration
```json
{
  "team_name": "string",
  "members": ["string"],
  "project_title": "string"
}
```

### RewardRequest
```json
{
  "request_id": "string",
  "outcome": "string"
}
```

### RewardResponse
```json
{
  "reward_value": 0.0,
  "feedback": "string"
}
```

### LogRequest
```json
{
  "timestamp": "string",
  "level": "string",
  "message": "string",
  "additional_data": {}
}
```

### LogEntry
```json
{
  "timestamp": "string",
  "level": "string",
  "message": "string"
}
```

## Integration Notes

### For Frontend Developers
1. All endpoints return JSON responses
2. Use `Content-Type: application/json` for POST requests
3. Handle HTTP error status codes appropriately
4. The `/docs` endpoint provides interactive API documentation

### For Backend Integration
1. The API is deployed on Render at https://ai-agent-x2iw.onrender.com
2. Webhook endpoints are available for automation
3. All major events are logged to the BHIV Bucket
4. The health endpoint can be used for monitoring

### For N8N Workflows
1. Use `/admin/webhook/hackaverse/registration` for team registration automation
2. All webhook responses include status information
3. Failed requests are logged for debugging