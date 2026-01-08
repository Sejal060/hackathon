# Phase B Handover Documentation

## Overview
This document provides handover information for Phase B of the HackaVerse backend implementation, focusing on production readiness, degraded mode handling, and deployment stability.

## Key Changes Implemented

### 1. Database Connection and Degraded Mode
- **File**: `src/database.py`
- **Changes**:
  - Added global variables: `DB_AVAILABLE`, `DB_ERROR_TYPE`
  - Implemented environment-aware startup behavior
  - In `ENV=development/test`: Startup continues with warnings on DB failure
  - In `ENV=production`: Startup fails immediately if DB unavailable
  - `get_db()` throws HTTP 503 when DB unavailable in degraded mode

### 2. Enhanced Health Endpoint
- **Endpoint**: `GET /system/health`
- **Response Format**:
  ```json
  {
    "success": true,
    "message": "System health check",
    "data": {
      "uptime": "123.45 seconds",
      "version": "v3",
      "db_connected": true,
      "degraded_mode": false,
      "env": "development",
      "db_error_type": null,
      "request_signing": "enabled",  // or "disabled" based on SECURITY_SECRET_KEY
      "replay_protection": "enabled",  // or "disabled" based on SECURITY_SECRET_KEY
      "rate_limiting": "enabled",
      "role_scoped_keys": "enabled"
    }
  }
  ```

### 3. Dependency Resolution
- **File**: `requirements.txt`
- **Changes**:
  - Removed unused/conflicting packages: `langchain`, `langchain-groq`, `langchain-text-splitters`, `langsmith`
  - Kept compatible versions: `langchain-core==0.3.78`, `langgraph==0.2.39`

### 4. Environment Variable Validation
- **File**: `src/main.py`
- **Changes**:
  - Added validation for `MONGODB_URI` and `BUCKET_DB_NAME`
  - Production mode: Fails fast on missing required variables
  - Development mode: Warns but continues

### 5. Render Deployment Configuration
- **File**: `render.yaml`
- **Changes**:
  - Added `ENV=production` for production deployments
  - Corrected `MONGODB_URI` environment variable mapping
  - Ensures clean startup without crash loops

### 6. Security Hardening Features
- **Files**: `src/security.py`, `src/middleware.py`, `src/main.py`, `src/routes/system.py`
- **Features Implemented**:
  - **Request Signing (HMAC)**: HMAC-SHA256 signature validation using `SECURITY_SECRET_KEY` (enforced when env var is set)
  - **Replay Protection**: Nonce-based protection with 5-minute TTL (enforced when `SECURITY_SECRET_KEY` is set)
  - **Role-Scoped API Keys**: API keys mapped to `agent` or `admin` roles
  - **Rate Limiting**: 60 requests/minute per API key, 10 requests/minute for `/admin` routes
- **Backward Compatibility**: When `SECURITY_SECRET_KEY` is not set, requests work without security headers
- **Health Endpoint**: Updated to show security feature status (enabled/disabled based on env var)

## QA Test Payloads

### Agent Endpoint
```bash
curl -X POST http://localhost:8001/agent/ \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "test_team_123",
    "prompt": "How to implement user authentication?",
    "metadata": {"project_type": "web_app"}
  }'
```
**Expected Response**: 200 OK with processed input, action, result, reward

### Team Registration
```bash
curl -X POST http://localhost:8001/admin/registration \
  -H "Content-Type: application/json" \
  -H "X-API-Key: production_secret_key_2024" \
  -d '{
    "team_name": "Innovators",
    "members": ["Alice", "Bob", "Charlie"],
    "project_title": "AI Mental Health Companion"
  }'
```
**Expected Response**: 200 OK with team_id

### Health Check
```bash
curl http://localhost:8001/system/health
```
**Expected Response**: 200 OK with database status information

## Deployment Instructions

### Local Development
```bash
export ENV=development
export MONGODB_URI=mongodb://localhost:27017
export BUCKET_DB_NAME=blackholeinifverse60_db_user
uvicorn src.main:app --reload
```

### Production (Render)
- Deploy via `render.yaml`
- Environment variables set automatically
- Health check path: `/system/health`

## Error Scenarios and Handling

### Database Unavailable (Development)
- App starts with warnings
- Health endpoint shows `degraded_mode: true`
- Agent endpoints return 503 with clear error message

### Database Unavailable (Production)
- App fails to start with clear error message
- Prevents deployment of broken instances

### Missing Environment Variables (Production)
- App fails to start immediately
- Clear error messages for missing `MONGODB_URI` or `BUCKET_DB_NAME`

## Monitoring and Troubleshooting

### Health Check Values
- `db_connected`: true/false
- `degraded_mode`: true if DB unavailable
- `env`: "development" or "production"
- `db_error_type`: "auth", "network", "dns", "unknown", or null

### Common Issues
1. **Cold Start Crashes**: Fixed by environment-aware startup logic
2. **503 Loops**: Prevented by fail-fast in production
3. **Dependency Conflicts**: Resolved by cleaning requirements.txt

## Next Steps
- Monitor production deployments for stability
- Implement authentication if required
- Add more detailed logging for production monitoring
- Consider adding database connection pooling metrics

## Failure Handling & Retry Policy

### Timeout Behavior
- **Database Connection Timeout**: 5 seconds for initial connection attempts
- **Database Query Timeout**: 5 seconds for read/write operations
- **HTTP Request Timeout**: 30 seconds for external API calls (e.g., BHIV Core communication)
- **Health Check Timeout**: 5 seconds for system health verification

### Retry Limits
- **Database Connection Retries**: 5 attempts with 2-second delays between retries
- **External API Retries**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Bucket Relay Retries**: 2 attempts for log/event transmission failures

### Distinction Between Recoverable vs Fatal Failures
- **Recoverable Failures**:
  - Temporary network timeouts (< 30s)
  - Database connection drops (auto-reconnect enabled)
  - Rate limiting (429 responses with retry-after header)
  - External API temporary unavailability (5xx with retry-after)
- **Fatal Failures**:
  - Authentication failures (401/403)
  - Invalid request data (400)
  - Resource not found (404)
  - Database authentication errors
  - Configuration errors (missing required environment variables)

### Error Response Codes
- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Missing/invalid API key or security headers
- **403**: Forbidden - Insufficient permissions for requested operation
- **404**: Not Found - Endpoint or resource does not exist
- **409**: Conflict - Replay attack detected or nonce reuse
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Unexpected system failures
- **503**: Service Unavailable - Database unavailable in production

## Contact
For issues or questions, refer to the integration notes in `INTEGRATION_NOTES.md` or contact the development team.