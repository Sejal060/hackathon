# HackaVerse Integration Notes

## For Yash (Frontend Integration)

### Key Endpoints
1. **Agent Processing**: `POST /agent/`
   - Use for submitting team prompts and getting AI responses
   - Include `team_id`, `prompt`, and optional `metadata`

2. **Team Registration**: `POST /admin/webhook/hackaverse/registration`
   - N8N webhook endpoint for new team registration
   - Payload: `{"team_name": "...", "members": [...], "project_title": "..."}`

3. **Health Check**: `GET /system/health`
   - Use to verify backend availability

### Example Usage
```javascript
// Submit a prompt to the agent
fetch('https://ai-agent-x2iw.onrender.com/agent/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    team_id: 'team_alpha',
    prompt: 'How to implement authentication?',
    metadata: {project_type: 'web_app'}
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## For Vinayak (Backend/Core Integration)

### Core Connector
- **File**: `src/core_connector.py`
- **Function**: `connect_to_core(payload)`
- **Mock URL**: `http://localhost:8002/process`
- **Replace with actual BHIV Core endpoint when available**

### Bucket Connector
- **File**: `src/bucket_connector.py`
- **Function**: `relay_to_bucket(log_data)`
- **MongoDB Connection**: Uses `MONGO_URI` from environment variables

### Micro Flow Logging
All major operations are logged with:
- **Intent**: What operation is being performed
- **Actor**: Which component is performing the operation
- **Context**: Details about the operation
- **Outcome**: Success/failure status

### Key Integration Points
1. **Use `/agent` for submissions**: All team prompts should be sent to this endpoint
2. **Logs via `/admin/logs`**: Manual log entries can be submitted here
3. **Registration via webhook**: N8N workflow hits `/admin/webhook/hackaverse/registration`

## Environment Variables
- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `BHIV_CORE_URL`: Core service URL (placeholder in current deployment)

## Deployment Notes
- **Render URL**: https://ai-agent-x2iw.onrender.com
- **GitHub Repo**: https://github.com/Sejal060/hackathon.git
- **Branch**: feature/hackaverse-v2-integration (to be merged to main)

## Testing
All endpoints have been tested and return 200 OK:
- ✅ `/agent/` (POST)
- ✅ `/admin/reward` (POST)
- ✅ `/admin/logs` (POST)
- ✅ `/admin/register` (POST)
- ✅ `/admin/webhook/hackaverse/registration` (POST)
- ✅ `/system/health` (GET)
- ✅ `/ping` (GET)
- ✅ `/` (GET)