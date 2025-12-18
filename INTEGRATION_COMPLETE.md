# INTEGRATION_COMPLETE.md

This document defines the frozen backend contract for frontend integration. These are the exact request and response formats that the frontend should use.

## Registration Endpoint

**POST /admin/register**

Request:
```json
{
  "team_name": "Team Alpha",
  "members": ["Alice", "Bob", "Charlie"],
  "project_title": "AI-Powered Solution"
}
```

Response:
```json
{
  "success": true,
  "message": "Team registered successfully",
  "data": {
    "team_id": "team_alpha"
  }
}
```

## Agent Chat Endpoint

**POST /agent/**

Request:
```json
{
  "team_id": "team_alpha",
  "prompt": "How do I submit my project?",
  "metadata": {
    "context": "project submission"
  }
}
```

Response:
```json
{
  "processed_input": "processed input",
  "action": "action plan",
  "result": "execution result",
  "reward": 1.0,
  "core_response": null
}
```

## Reward Endpoint

**POST /admin/reward**

Request:
```json
{
  "request_id": "req_12345",
  "outcome": "success"
}
```

Response:
```json
{
  "reward_value": 1.0,
  "feedback": "Great job!"
}
```

## Logs Endpoint

**POST /admin/logs**

Request:
```json
{
  "timestamp": "2025-01-01T10:00:00Z",
  "level": "INFO",
  "message": "User performed action",
  "additional_data": {
    "user_id": "user_123"
  }
}
```

Response:
```json
{
  "success": true,
  "message": "Logs relayed successfully",
  "data": {
    "status": "logged",
    "result": "Log relayed successfully"
  }
}
```

**GET /system/logs**

Request:
```json
GET /system/logs?limit=50
```

Response:
```json
{
  "success": true,
  "message": "Logs retrieved successfully",
  "data": {
    "logs": [
      {
        "_id": "507f1f77bcf86cd799439011",
        "timestamp": "2025-01-01T10:00:00Z",
        "level": "INFO",
        "message": "User performed action"
      }
    ]
  }
}
```

## Health Endpoint

**GET /system/health**

Response:
```json
{
  "success": true,
  "message": "System is healthy",
  "data": {
    "uptime": "120.50 seconds",
    "version": "v3"
  }
}
```

## Backend URL and CORS Configuration

**Backend URL**: https://ai-agent-x2iw.onrender.com

**Allowed CORS Origins**:
- http://localhost:3000
- https://<yash-frontend-url> (Replace with actual frontend URL)

## Instructions for Yash

Use only these payloads. If anything breaks, report immediately.