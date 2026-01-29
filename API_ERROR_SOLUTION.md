# API Error Solution: 400 Bad Request

## Problem Description
The PowerShell command was failing with a 400 Bad Request error when trying to register a team:

```powershell
Invoke-WebRequest : The remote server returned an error: (400) Bad Request.
```

## Root Cause Analysis

### 1. Incorrect Endpoint URL
**Original URL:** `https://ai-agent-x2iw.onrender.com/workflows/team-registration`
**Issue:** The PowerShell script was using `/registration` instead of `/workflows/team-registration`

### 2. API Key Configuration
The API key `2b899caf7e3aea924c96761326bdded5162da31a9d1fdba59a2a451d2335c778` needs to be set as the `API_KEY` environment variable in the deployed application.

## Solution

### 1. Fixed PowerShell Script
Updated [`test_team_registration.ps1`](hackathon/test_team_registration.ps1) with the correct endpoint URL:

```powershell
$apiUrl = "https://ai-agent-x2iw.onrender.com/workflows/team-registration"
```

### 2. API Key Configuration
The API key must be set in the environment where the application is deployed:

**For Render deployment:**
1. Go to your Render dashboard
2. Navigate to your service settings
3. Add environment variable: `API_KEY=2b899caf7e3aea924c96761326bdded5162da31a9d1fdba59a2a451d2335c778`

**For local development:**
Add to `.env` file:
```
API_KEY=2b899caf7e3aea924c96761326bdded5162da31a9d1fdba59a2a451d2335c778
```

### 3. Required Payload Structure
The team registration endpoint expects the following payload structure:

```json
{
  "team_name": "string",           // Required
  "members": ["string"],           // Required (array of strings)
  "project_title": "string",       // Required
  "tenant_id": "string",           // Optional
  "workspace_id": "string",        // Optional
  "event_id": "string"             // Optional
}
```

## Testing Tools Created

### 1. Python Test Script
[`test_api_registration.py`](hackathon/test_api_registration.py) - Comprehensive Python test script

### 2. Comprehensive Test Script
[`comprehensive_api_test.py`](hackathon/comprehensive_api_test.py) - Tests multiple scenarios and endpoints

### 3. Bash/Curl Test Script
[`test_api_curl.sh`](hackathon/test_api_curl.sh) - Command-line testing with curl

## How to Test

### Using PowerShell (Fixed)
```powershell
.\test_team_registration.ps1
```

### Using Python
```bash
python test_api_registration.py
```

### Using Bash
```bash
chmod +x test_api_curl.sh
./test_api_curl.sh
```

### Using curl directly
```bash
curl -X POST "https://ai-agent-x2iw.onrender.com/workflows/team-registration" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 2b899caf7e3aea924c96761326bdded5162da31a9d1fdba59a2a451d2335c778" \
  -d '{
    "team_name": "Tenant Test Team",
    "members": ["Alice"],
    "project_title": "MultiTenant Verification",
    "tenant_id": "tenant_123",
    "workspace_id": "workspace_456",
    "event_id": "event_789"
  }'
```

## Verification Steps

1. **Set the API key** in your deployment environment
2. **Test the health endpoint**: `GET /ping`
3. **Test the workflows health**: `GET /workflows/health`
4. **Test team registration** with the corrected URL and payload

## Expected Response

Successful team registration should return:
```json
{
  "status": "success",
  "workflow_type": "team_registration",
  "message": "Team registration completed successfully",
  "result": {
    "team_id": "generated-team-id",
    "registration_time": "2024-01-10T10:00:00"
  },
  "timestamp": "2024-01-10T10:00:00"
}
```

## Troubleshooting

If you still get a 400 error:

1. **Verify API key** is correctly set in environment
2. **Check payload structure** matches the required format
3. **Test with minimal payload** (only required fields)
4. **Check server logs** for detailed error messages
5. **Verify LangGraph workflows** are properly configured

## Additional Endpoints

- `GET /ping` - Health check
- `GET /workflows/health` - Workflows health check
- `GET /workflows/list` - List available workflows
- `POST /workflows/mentorbot` - MentorBot workflow
- `POST /workflows/judging-reminder` - Judging reminder workflow