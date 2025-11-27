# HackaVerse Backend - Integration Guide

## Overview

This document provides instructions for integrating with the HackaVerse backend API. The backend provides several endpoints for hackathon management including team registration, agent processing, reward calculation, and logging.

## Base URL

```
https://ai-agent-x2iw.onrender.com
```

For local development:
```
http://localhost:8001
```

## Authentication

All administrative endpoints require an API key in the `X-API-Key` header:

```
X-API-Key: production_secret_key_2024
```

## Endpoints

### 1. Health Check
**GET** `/system/health`

Returns the health status of the system.

**Response:**
```json
{
  "status": "healthy",
  "version": "v2.0",
  "timestamp": "2024-01-01T12:00:00Z",
  "platform": "Windows 10"
}
```

### 2. Team Registration
**POST** `/admin/register`

Register a new team for the hackathon.

**Request:**
```json
{
  "team_name": "Innovators",
  "members": ["Alice", "Bob", "Charlie"],
  "project_title": "AI Assistant"
}
```

**Response:**
```json
{
  "message": "Team registered successfully",
  "team_id": "team_innovators"
}
```

### 3. Agent Processing
**POST** `/agent/`

Process a request through the AI agent system.

**Request:**
```json
{
  "team_id": "team_innovators",
  "prompt": "How do I implement user authentication?",
  "metadata": {
    "project_type": "web_application",
    "tech_stack": "FastAPI, MongoDB"
  }
}
```

**Response:**
```json
{
  "processed_input": "How do I implement user authentication?",
  "action": "Research best practices for user authentication in web applications",
  "result": "For implementing user authentication in a FastAPI application with MongoDB...",
  "reward": 0.85,
  "core_response": {
    "status": "success",
    "data": "..."
  }
}
```

### 4. Reward Calculation
**POST** `/admin/reward`

Calculate and apply rewards based on action outcomes.

**Request:**
```json
{
  "request_id": "req_12345",
  "outcome": "success"
}
```

**Response:**
```json
{
  "reward_value": 0.85,
  "feedback": "Positive reward assigned for successful completion"
}
```

### 5. Log Submission
**POST** `/admin/logs`

Submit logs to the system.

**Request:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "message": "Team Innovators completed authentication implementation",
  "additional_data": {
    "team_id": "team_innovators",
    "milestone": "authentication"
  }
}
```

**Response:**
```json
{
  "status": "logged",
  "result": "Log relayed successfully"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `422` - Validation Error
- `500` - Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## CORS Configuration

The backend is configured to accept requests from all origins in development. For production, specific domains should be configured in the `ALLOWED_ORIGINS` environment variable.

## Environment Variables

For local development, create a `.env` file with the following variables:

```env
API_KEY=your_secret_api_key_here
BHIV_CORE_URL=http://localhost:8002/reason
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_api_key_here
ALLOWED_ORIGINS=*
```

## Frontend Integration Example

Here's a simple example of how to integrate with the backend from JavaScript:

```javascript
const BASE_URL = 'https://ai-agent-x2iw.onrender.com';
const API_KEY = 'production_secret_key_2024';

// Register a team
async function registerTeam(teamData) {
  const response = await fetch(`${BASE_URL}/admin/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify(teamData)
  });
  
  return response.json();
}

// Process an agent request
async function processAgentRequest(requestData) {
  const response = await fetch(`${BASE_URL}/agent/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify(requestData)
  });
  
  return response.json();
}
```

## Deployment

The backend is deployed on Render and is accessible at:
```
https://ai-agent-x2iw.onrender.com
```

The service automatically deploys from the main branch on GitHub.

## Support

For questions about this integration, contact:
- **Sejal Dongre** - Backend Lead
- **Yash** - Frontend Integration
- **Vinayak** - QA & Task Bank

## Version Information

- **Current Version**: v2.0
- **Last Updated**: 2025-11-10
- **Status**: ✅ READY FOR HANDOFF