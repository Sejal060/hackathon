Integration Guide for Sejal's AI Agent System
This guide is for Yash (frontend team) to integrate the AI Agent System backend into the React + Tailwind CSS frontend via Akash’s /api/agent middleware. The backend is live at https://ai-agent-x2iw.onrender.com and provides RESTful APIs with auto-generated OpenAPI docs.
Setup
Local Development

Run Locally: Activate virtual env (myenv\Scripts\activate) and start server:uvicorn src.main:app --reload


Swagger UI: Access at http://127.0.0.1:8000/docs for interactive testing.
OpenAPI Schema: Download raw schema at http://127.0.0.1:8000/openapi.json.

Live Deployment

Live URL: https://ai-agent-x2iw.onrender.com
Docs: https://ai-agent-x2iw.onrender.com/docs (interactive Swagger UI).
Schema: https://ai-agent-x2iw.onrender.com/openapi.json.
Env Vars: Configure GROQ_API_KEY in .env (see RENDER_DEPLOYMENT_GUIDE.md).

Middleware Integration

Connect to Akash’s /api/agent endpoint (core.gurukul-ai.in/api/agent) which forwards requests to this backend.
Use the same JSON schemas and error codes as below.

API Endpoints
1. GET /agent

Purpose: Send a user prompt to the agent.
Request:
URL: https://ai-agent-x2iw.onrender.com/agent?input={prompt}
Example: https://ai-agent-x2iw.onrender.com/agent?input=plan%20a%20trip


Response (200 OK):{
  "processed_input": "plan a trip",
  "action": "Check weather -> Book transport",
  "result": "Executed: Check weather | Executed: Book transport",
  "reward": 1.0
}


cURL Example:curl "https://ai-agent-x2iw.onrender.com/agent?input=plan%20a%20trip"


Postman:
Method: GET
URL: https://ai-agent-x2iw.onrender.com/agent?input=plan a trip
Response: See above JSON.


React Fetch Example:fetch(`https://ai-agent-x2iw.onrender.com/agent?input=${encodeURIComponent(prompt)}`)
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.log("Agent Response:", data);
    // Update UI with data.action, data.result, etc.
  })
  .catch(error => console.error("Fetch error:", error));



2. POST /agent

Purpose: Send a prompt with optional context (e.g., location).
Request:
URL: https://ai-agent-x2iw.onrender.com/agent
Body:{
  "user_input": "plan a trip",
  "context": {"location": "Himalayas", "priority": "high"}
}




Response (200 OK):{
  "processed_input": "plan a trip",
  "action": "Check weather -> Book transport (location=Himalayas, priority=high)",
  "result": "Executed: Check weather | Executed: Book transport",
  "reward": 1.0
}


cURL Example:curl -X POST "https://ai-agent-x2iw.onrender.com/agent" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "plan a trip", "context": {"location": "Himalayas", "priority": "high"}}'


Postman:
Method: POST
URL: https://ai-agent-x2iw.onrender.com/agent
Body (raw JSON):{"user_input": "plan a trip", "context": {"location": "Himalayas", "priority": "high"}}


Response: See above JSON.


React Fetch Example:fetch("https://ai-agent-x2iw.onrender.com/agent", {
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



3. POST /reward

Purpose: Submit an action outcome to calculate a reward.
Request:
URL: https://ai-agent-x2iw.onrender.com/reward
Body:{
  "action": "step1|step2",
  "outcome": "success"
}




Response (200 OK):{
  "reward_value": 3.0,
  "feedback": "Success"
}


cURL Example:curl -X POST "https://ai-agent-x2iw.onrender.com/reward" \
  -H "Content-Type: application/json" \
  -d '{"action": "step1|step2", "outcome": "success"}'


Postman:
Method: POST
URL: https://ai-agent-x2iw.onrender.com/reward
Body (raw JSON):{"action": "step1|step2", "outcome": "success"}


Response: See above JSON.


React Fetch Example:fetch("https://ai-agent-x2iw.onrender.com/reward", {
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



Frontend Integration Tips

React Component: Use a state management library (e.g., Redux) to store action, result, and reward.
Streaming: If Akash implements streaming, use response.body.getReader() for real-time updates.
UI Display: Render action as a plan list, result as executed steps, and reward as a score.
Error Feedback: Show 422/500 errors with Tailwind CSS alerts (e.g., bg-red-500 text-white).

Postman Collection

Download postman_collection.json from the repo and import into Postman.
Includes pre-configured requests for all endpoints with sample data.

Troubleshooting

422 Validation Error: Ensure input or user_input has at least 1 character. Check JSON structure.
500 Internal Error: Contact Sejal or check logs via /logs endpoint.
Timeout: Increase fetch timeout or retry logic in frontend.

Additional Notes

All endpoints use Pydantic-validated JSON schemas (see /openapi.json).
Connect to Akash’s /api/agent for production use, forwarding to this URL.
Test with /docs for real-time validation.
