# HackaVerse – Frontend ↔ Backend Integration Contract

Backend Base URL:
https://ai-agent-x2iw.onrender.com

Frontend:
- Localhost: http://localhost:3000
- Deployed: https://blackholeinfiverse66.github.io

CORS: Verified

---

## 1. System Health

### Endpoint
GET /system/health

### Request
No body

### Response (200)
{
  "success": true,
  "message": "System is healthy",
  "data": {
    "uptime": "4550.24 seconds",
    "version": "v3"
  }
}

Frontend Usage:
Used for health widget and startup checks.

---

## 2. Register

### Endpoint
POST /admin/register

### Request
{
  "team_name": "Test Team",
  "members": ["Alice", "Bob"],
  "project_title": "Test Project"
}

### Response
- 200 / 201: Team registered successfully
- 400: Validation error or missing API key
- 404: Endpoint not implemented (frontend mock mode)

Frontend Status:
UI wired, backend partially implemented.

---

## 3. Agent

### Endpoint
POST /agent

### Request
{
  "team_id": "team123",
  "prompt": "How do I submit my project?"
}

### Response (200)
{
  "processed_input": "processed input",
  "action": "action plan",
  "result": "execution result",
  "reward": 1.0,
  "core_response": null
}

Frontend Usage:
Used by HackaAgent chat interface.

---

## 4. Admin Reward

### Endpoint
POST /admin/reward

### Status
Protected / Not yet integrated

Frontend:
Admin UI placeholder exists.
Backend logic pending or access-restricted.

---

## 5. Logs

### Endpoint
GET /system/logs

### Status
Accessible with proper authentication.

Frontend:
Logs page wired; backend access restricted.

---

## Integration Summary

- Frontend successfully connected to production backend
- Health checks operational
- AI agent integrated
- Auth flows mocked for testing
- Admin and logs endpoints documented

Integration Owner: Sejal  
Frontend: Yash  
QA: Vinayak