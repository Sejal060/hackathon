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
   - Use to verify backend availability and get system status

4. **Reward System**: `POST /admin/reward`
   - Apply rewards based on team performance
   - Include `request_id` and `outcome`

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

// Register a team via webhook
fetch('https://ai-agent-x2iw.onrender.com/admin/webhook/hackaverse/registration', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    team_name: 'Innovators',
    members: ['Alice', 'Bob'],
    project_title: 'AI Assistant'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Check system health
fetch('https://ai-agent-x2iw.onrender.com/system/health')
.then(response => response.json())
.then(data => console.log(data));
```

### Frontend Integration Guidelines
1. **Error Handling**: Always handle HTTP error responses appropriately
2. **Loading States**: Show loading indicators during API requests
3. **Validation**: Validate user input before sending to backend
4. **Caching**: Cache health check results to reduce unnecessary requests

## For Vinayak (Backend/Core Integration)

### Core Connector
- **File**: `src/core_connector.py`
- **Function**: `connect_to_core(payload)`
- **Environment Variable**: `BHIV_CORE_URL` (default: http://localhost:8002/process)
- **Replace with actual BHIV Core endpoint when available**

### Bucket Connector
- **File**: `src/bucket_connector.py`
- **Function**: `relay_to_bucket(log_data)`
- **Environment Variables**: 
  - `MONGO_URI` (default: mongodb://localhost:27017)
  - `BUCKET_DB_NAME` (default: blackholeinifverse60_db_user)
- **Fallback**: File-based logging if MongoDB is unavailable

### Micro Flow Logging (KSML Layer)
All major operations are logged with structured data:
- **Intent**: What operation is being performed (e.g., "agent_request", "core_connection")
- **Actor**: Which component is performing the operation (e.g., "team", "core_connector")
- **Context**: Details about the operation
- **Outcome**: Success/failure status with specific error types

### Key Integration Points
1. **Use `/agent` for submissions**: All team prompts should be sent to this endpoint
2. **Logs via `/admin/logs`**: Manual log entries can be submitted here
3. **Registration via webhook**: N8N workflow hits `/admin/webhook/hackaverse/registration`
4. **Reward system**: Use `/admin/reward` to apply rewards based on outcomes

### Error Handling and Retry Logic
1. **Core Connector**: Implements timeout (10s) and various error handling strategies
2. **Bucket Connector**: Fallback to file logging if MongoDB is unavailable
3. **Retry Logic**: Core connector handles timeouts and connection errors gracefully

## Environment Variables
- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `BHIV_CORE_URL`: Core service URL (default: http://localhost:8002/process)
- `BUCKET_DB_NAME`: MongoDB database name (default: blackholeinifverse60_db_user)

## Deployment Notes
- **Render URL**: https://ai-agent-x2iw.onrender.com
- **GitHub Repo**: https://github.com/Sejal060/hackathon.git
- **Branch**: feature/hackaverse-v2-integration (to be merged to main)
- **Port**: Configured via `$PORT` environment variable on Render

## Testing Endpoints
All endpoints have been tested and return 200 OK:
- ✅ `/agent/` (POST)
- ✅ `/admin/reward` (POST)
- ✅ `/admin/logs` (POST)
- ✅ `/admin/register` (POST)
- ✅ `/admin/webhook/hackaverse/registration` (POST)
- ✅ `/system/health` (GET)
- ✅ `/ping` (GET)
- ✅ `/` (GET)

### Testing with curl
```bash
# Test agent endpoint
curl -X POST https://ai-agent-x2iw.onrender.com/agent/ \
  -H "Content-Type: application/json" \
  -d '{"team_id":"test_team","prompt":"Hello, world!","metadata":{}}'

# Test health endpoint
curl https://ai-agent-x2iw.onrender.com/system/health

# Test registration webhook
curl -X POST https://ai-agent-x2iw.onrender.com/admin/webhook/hackaverse/registration \
  -H "Content-Type: application/json" \
  -d '{"team_name":"Test Team","members":["Alice","Bob"],"project_title":"Test Project"}'
```

## Monitoring and Observability
1. **Health Endpoint**: `/system/health` provides system status information
2. **Structured Logging**: All operations are logged with consistent structure
3. **Error Tracking**: Different error types are categorized for easier debugging
4. **Performance Metrics**: Request processing times are implicitly tracked through logs

## Security Considerations
1. **CORS**: Currently allows all origins (to be restricted in production)
2. **Input Validation**: All endpoints use Pydantic models for validation
3. **Error Information**: Error responses don't expose sensitive system information
4. **No Authentication**: Currently no authentication (to be added based on requirements)