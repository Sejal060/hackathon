Integration Guide for Sejal's AI Agent System
This guide is for Yash (frontend team) to integrate the AI Agent System backend into the React + Tailwind CSS frontend via Akash's /api/agent middleware. The backend is live at https://ai-agent-x2iw.onrender.com and provides RESTful APIs with auto-generated OpenAPI docs.

## Setup

### Local Development

Run Locally: Activate virtual env (myenv\Scripts\activate) and start server:
```
uvicorn src.main:app --reload
```

Swagger UI: Access at http://127.0.0.1:8000/docs for interactive testing.
OpenAPI Schema: Download raw schema at http://127.0.0.1:8000/openapi.json.

### Live Deployment

Live URL: https://ai-agent-x2iw.onrender.com
Docs: https://ai-agent-x2iw.onrender.com/docs (interactive Swagger UI).
Schema: https://ai-agent-x2iw.onrender.com/openapi.json.
Env Vars: Configure GROQ_API_KEY in .env (see RENDER_DEPLOYMENT_GUIDE.md).

## Middleware Integration

Connect to Akash's /api/agent endpoint (core.gurukul-ai.in/api/agent) which forwards requests to this backend.
Use the same JSON schemas and error codes as below.

## API Endpoints

### 1. GET /agent

Purpose: Send a user prompt to the agent.
Request:
URL: https://ai-agent-x2iw.onrender.com/agent?input={prompt}
Example: https://ai-agent-x2iw.onrender.com/agent?input=plan%20a%20trip

Response (200 OK):
```json
{
  "processed_input": "plan a trip",
  "action": "Check weather -> Book transport",
  "result": "Executed: Check weather | Executed: Book transport",
  "reward": 1.0
}
```

cURL Example:
```bash
curl "https://ai-agent-x2iw.onrender.com/agent?input=plan%20a%20trip"
```

Postman:
Method: GET
URL: https://ai-agent-x2iw.onrender.com/agent?input=plan a trip
Response: See above JSON.

React Fetch Example:
```javascript
fetch(`https://ai-agent-x2iw.onrender.com/agent?input=${encodeURIComponent(prompt)}`)
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.log("Agent Response:", data);
    // Update UI with data.action, data.result, etc.
  })
  .catch(error => console.error("Fetch error:", error));
```

### 2. POST /agent

Purpose: Send a prompt with optional context (e.g., location).
Request:
URL: https://ai-agent-x2iw.onrender.com/agent
Body:
```json
{
  "user_input": "plan a trip",
  "context": {"location": "Himalayas", "priority": "high"}
}
```

Response (200 OK):
```json
{
  "processed_input": "plan a trip",
  "action": "Check weather -> Book transport (location=Himalayas, priority=high)",
  "result": "Executed: Check weather | Executed: Book transport",
  "reward": 1.0
}
```

cURL Example:
```bash
curl -X POST "https://ai-agent-x2iw.onrender.com/agent" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "plan a trip", "context": {"location": "Himalayas", "priority": "high"}}'
```

Postman:
Method: POST
URL: https://ai-agent-x2iw.onrender.com/agent
Body (raw JSON):
```json
{"user_input": "plan a trip", "context": {"location": "Himalayas", "priority": "high"}}
```

Response: See above JSON.

React Fetch Example:
```javascript
fetch("https://ai-agent-x2iw.onrender.com/agent", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({user_input: prompt, context: {location: "Himalayas", priority: "high"}})
})
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.log("Agent Response:", data);
    // Update UI with data.action, data.result, etc.
  })
  .catch(error => console.error("Fetch error:", error));
```

### 3. POST /reward

Purpose: Submit an action outcome to calculate a reward.
Request:
URL: https://ai-agent-x2iw.onrender.com/reward
Body:
```json
{
  "action": "step1|step2",
  "outcome": "success"
}
```

Response (200 OK):
```json
{
  "reward_value": 3.0,
  "feedback": "Success"
}
```

cURL Example:
```bash
curl -X POST "https://ai-agent-x2iw.onrender.com/reward" \
  -H "Content-Type: application/json" \
  -d '{"action": "step1|step2", "outcome": "success"}'
```

Postman:
Method: POST
URL: https://ai-agent-x2iw.onrender.com/reward
Body (raw JSON):
```json
{"action": "step1|step2", "outcome": "success"}
```

Response: See above JSON.

React Fetch Example:
```javascript
fetch("https://ai-agent-x2iw.onrender.com/reward", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({action: "step1|step2", outcome: "success"})
})
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.log("Reward Response:", data);
    // Update UI with data.reward_value, data.feedback
  })
  .catch(error => console.error("Fetch error:", error));
```

## N8N Automation

The system includes n8n workflow automation for various processes:

### Workflows
1. **Team Registration Workflow** (`n8n/workflows/team_registration.json`)
   - Trigger: Webhook
   - Action: Sends registration data to the `/agent` endpoint
   - Purpose: Automates team registration process

2. **Judging Reminder Workflow** (`n8n/workflows/judging_reminder.json`)
   - Trigger: Schedule trigger (cron)
   - Action: Sends email notifications to judges
   - Purpose: Reminds judges to evaluate submissions

3. **MentorBot Prompt Workflow** (`n8n/workflows/mentorbot_prompt.json`)
   - Trigger: Webhook
   - Action: Sends mentor requests to the `/agent` endpoint
   - Purpose: Provides automated mentor support

### How to Import Workflows
1. Open n8n (local installation or cloud version)
2. Go to **Settings** → **Import**
3. Paste the JSON content from any of the workflow files in `n8n/workflows/`
4. Save and activate the workflow

### Testing Workflows
To test these workflows without running n8n:
1. Use the test script `scripts/test_n8n_workflows.py`
2. This script simulates webhook POSTs to your FastAPI endpoints
3. Check the responses to verify expected behavior

### Example Webhook URLs
After importing and activating workflows in n8n, you'll get webhook URLs like:
```
https://your-n8n-instance.web.app/webhook/team-registration
https://your-n8n-instance.web.app/webhook/mentor-request
```

### Example Payloads
#### Team Registration Payload
```json
{
  "user_input": "Register team test_team",
  "context": {
    "team_id": "test_team"
  }
}
```

#### Mentor Request Payload
```json
{
  "user_input": "How do I implement authentication in my FastAPI app?",
  "context": {
    "team_id": "team_123",
    "project_type": "web_application"
  }
}
```

### Screenshots and Logs
Workflow execution screenshots and logs are available in the `n8n/screenshots/` directory.
See `n8n/screenshots/README.md` for details.

## Tests and Coverage

The project includes a comprehensive test suite to ensure reliability:

### Test Coverage: **82.38%**

Tests are implemented for all core components:
- ✅ Storage Service (`tests/test_storage.py`)
- ✅ Transaction Manager (`tests/test_transaction_manager.py`)
- ✅ BHIV Connectors (`tests/test_bhiv_connectors.py`)
- ✅ API Endpoints (`tests/test_endpoints.py`)
- ✅ Reward System (`tests/test_reward.py`)
- ✅ Executor Module (`tests/test_executor.py`)
- ✅ Reasoning Module (`tests/test_reasoning.py`)
- ✅ Reinforcement Learning (`tests/test_rl.py`)

### Run Tests
```bash
# Run all tests with coverage
pytest tests/ --cov=src

# Run tests with detailed coverage reports
pytest tests/ --cov=src --cov-report=html --cov-report=xml
```

### CI/CD Integration
The GitHub Actions workflow in `.github/workflows/ci-cd.yaml` includes:
- Running all tests with coverage
- Generating XML and HTML coverage reports
- Uploading coverage reports as artifacts
- Uploading screenshots as artifacts
- Publishing coverage to Codecov (when configured)

### Test Results
```
===== 44 passed in 257.83s (0:04:17) ======
```

## Frontend Integration Tips

React Component: Use a state management library (e.g., Redux) to store action, result, and reward.
Streaming: If Akash implements streaming, use response.body.getReader() for real-time updates.
UI Display: Render action as a plan list, result as executed steps, and reward as a score.
Error Feedback: Show 422/500 errors with Tailwind CSS alerts (e.g., bg-red-500 text-white).

## Postman Collection

Download postman_collection.json from the repo and import into Postman.
Includes pre-configured requests for all endpoints with sample data.

## Troubleshooting

422 Validation Error: Ensure input or user_input has at least 1 character. Check JSON structure.
500 Internal Error: Contact Sejal or check logs via /logs endpoint.
Timeout: Increase fetch timeout or retry logic in frontend.

## Additional Notes

All endpoints use Pydantic-validated JSON schemas (see /openapi.json).
Connect to Akash's /api/agent for production use, forwarding to this URL.
Test with /docs for real-time validation.