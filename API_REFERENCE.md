# HackaVerse API Reference

## Overview
HackaVerse API v2.0 - Hackathon engine for agent processing, reward calculation, and logging.

## Base URL
Local: http://127.0.0.1:8001
Deployed: https://ai-agent-x2iw.onrender.com

## Authentication
No authentication required for current endpoints.

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
Calculate and apply rewards.

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

#### POST /admin/logs
Relay logs to bucket.

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

#### POST /admin/register
Register a new team.

**Response:**
```json
{
  "message": "Team registered successfully"
}
```

#### POST /admin/webhook/hackaverse/registration
N8N webhook for team registration.

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
  "status": "registered"
}
```

### System Endpoints

#### GET /system/health
Check system health.

**Response:**
```json
{
  "status": "healthy",
  "version": "v2",
  "timestamp": "string"
}
```

#### GET /ping
Basic health check.

**Response:**
```json
{
  "status": "ok"
}
```

#### GET /
Root endpoint.

**Response:**
```json
{
  "message": "FastAPI is running 🚀",
  "docs": "/docs"
}
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