# 🧠 Sejal's AI Hackathon System

An end-to-end intelligent hackathon management and reflection system integrating MCP Agents, BHIV Core, MongoDB, and N8N automation.

---

## 🚀 Project Overview

This system automates hackathon workflows — from team registration and project submissions to AI-based judging and mentor support — using modular MCP agents integrated with the **BHIV Core system**.

It includes:

* 🌐 **FastAPI backend** — handles team registration and AI reasoning via `/register` and `/agent`.
* 🧩 **MongoDB (BHIV Bucket)** — stores all reflections, logs, and simulation data.
* ⚙️ **N8N workflows** — automates team registration, reminders, and mentor prompts.
* 🤖 **Simulation script** — tests 5–10 team interactions automatically.
* 📊 **Streamlit dashboard** — displays reflection and log data visually.

---

## OpenAPI docs

Live docs URL: https://ai-agent-x2iw.onrender.com/docs

Sample cURL commands and expected HTTP responses:

```bash
# Get docs (after deployment)
curl -s https://YOUR_URL/openapi.json | jq '.paths | keys'

# Call agent
curl -X POST https://YOUR_URL/agent \
  -H "Content-Type: application/json" \
  -d '{"team_id":"team_42","submission_url":"https://..." }'
```

To verify docs locally:

```bash
# Using the provided script (Unix/Linux/Mac)
chmod +x scripts/check_docs.sh
./scripts/check_docs.sh

# Using the provided script (Windows)
scripts\check_docs.bat
```

---

## 🏗️ Project Structure

```
sejal060-hackathon/
├── src/
│   ├── main.py
│   ├── input_handler.py
│   ├── reasoning.py
│   ├── executor.py
│   ├── reward.py
│   └── schemas.py
├── n8n/
│   └── workflows/
│       ├── team_registration.json
│       ├── judging_reminder.json
│       └── mentorbot_prompt.json
├── simulate_teams.py
├── dashboard.py
├── .env.example
├── README.md
├── requirements.txt
└── docs/
    └── reflection.md
```

---

## ⚙️ Installation and Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sejal060/hackathon.git
cd hackathon
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate   # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗃️ Environment Variables

Copy `.env.example` → `.env` and make sure it contains:

```
BHIV_CORE_URL=http://localhost:8002/reason
MONGO_URI=mongodb://localhost:27017
```

---

## 🧪 Tests and Coverage

### Test Coverage: **91%**

Tests are implemented for all core components:

* ✅ Storage Service (`tests/test_storage.py`)
* ✅ Transaction Manager (`tests/test_transaction_manager.py`)
* ✅ BHIV Connectors (`tests/test_bhiv_connectors.py`)
* ✅ API Endpoints (`tests/test_endpoints.py`)
* ✅ Reward System (`tests/test_reward.py`)
* ✅ Executor Module (`tests/test_executor.py`)
* ✅ Reasoning Module (`tests/test_reasoning.py`)
* ✅ Reinforcement Learning (`tests/test_rl.py`)
* ✅ Agent Module (`tests/test_agent_additional.py`)
* ✅ Multi-Agent Module (`tests/test_multi_agent.py`)

### Run Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=src

# Run tests with detailed coverage reports
pytest tests/ --cov=src --cov-report=html --cov-report=xml
```

### Test Results
```
===== 60 passed in 261.62s (0:04:21) ======
```

### Coverage Details
```
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
src\__init__.py                           0      0   100%
src\agent.py                             24      0   100%
src\executor.py                          33      6    82%
src\input_handler.py                      4      0   100%
src\integrations\__init__.py              0      0   100%
src\integrations\bhiv_connectors.py      43      2    95%
src\main.py                             116      8    93%
src\multi_agent.py                       17      0   100%
src\reasoning.py                         35      8    77%
src\reward.py                            41      4    90%
src\routes.py                            40      5    88%
src\schemas.py                           13      0   100%
src\storage_service.py                   64      9    86%
src\transaction_manager.py               58      3    95%
---------------------------------------------------------
TOTAL                                   488     45    91%
```

---

## 🧩 Step-by-Step Execution

### **Step 1 — Start MongoDB**

```bash
net start MongoDB
```

Then open **MongoDB Compass** and connect:

```
mongodb://localhost:27017
```

You should see a database named **bhiv_db**.

---

### **Step 2 — Run FastAPI Backend**

```bash
uvicorn src.main:app --reload --port 8001
```

Open Swagger UI:
👉 [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

**Test Endpoints:**

#### `/register`

```json
{
  "team_name": "Test_Team",
  "members": ["Sejal", "Akshay", "Prajakta"],
  "project_title": "Smart AI Project"
}
```

#### `/agent`

```json
{
  "query": "Explain reflection logging in AI agents"
}
```

✅ Expected:

* Returns a success message
* New logs appear in MongoDB (`bhiv_db.logs`)

---

### **Step 3 — Run the Simulation**

```bash
python simulate_teams.py
```

✅ Expected:

* 5–10 teams simulated
* MongoDB Compass shows 10–20 new log entries
* No terminal errors

---

### **Step 4 — Launch the Dashboard**

```bash
streamlit run dashboard.py
```

Then open:
👉 [http://localhost:8501](http://localhost:8501)

✅ Expected:

* Displays total log count
* Shows reflection data (team names, timestamps, kinds, etc.)
* Shows visualizations:
  * Leaderboard (bar chart)
  * Score trend (line chart)
  * Acceptance rate (pie chart)
* Includes a refresh button to reload JSON data

---

### **Step 5 — N8N Automation**

The system includes N8N workflow automation:

```
n8n/
├── README.md
├── workflows/
│   ├── team_registration.json
│   ├── judging_reminder.json
│   └── mentorbot_prompt.json
└── screenshots/
```

#### Import Workflows

1. Open n8n (local installation or cloud version)
2. Go to **Settings** → **Import**
3. Paste the JSON content from any workflow file
4. Save and activate the workflow

#### Test Workflows

```bash
# Test N8N workflows with simulation script
python scripts/test_n8n_workflows.py
```

#### Workflows

1. **Team Registration** - Automates team registration via webhook
2. **Judging Reminder** - Sends email notifications to judges
3. **MentorBot Prompt** - Provides automated mentor support

---

## ☁️ Deployment

The backend is deployed on Render and is accessible at:

👉 **Live URL**: https://ai-agent-x2iw.onrender.com

### API Endpoints

* **API Base**: https://ai-agent-x2iw.onrender.com
* **Documentation**: https://ai-agent-x2iw.onrender.com/docs
* **OpenAPI Spec**: https://ai-agent-x2iw.onrender.com/openapi.json

### Example Usage

```bash
# Get API documentation
curl https://ai-agent-x2iw.onrender.com/docs

# Call agent endpoint
curl https://ai-agent-x2iw.onrender.com/agent \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_input":"Explain how to build a REST API with FastAPI","context":{"team_id":"demo_team","project_type":"web_application"}}'
```

### Deployment Process

1. Push code to the `main` branch on GitHub
2. Render automatically deploys the service using the configuration in `render.yaml`
3. Environment variables are configured in the Render dashboard

---

## 🧾 Verification Summary

| Component         | Status | Verification                       |
| ----------------- | ------ | ---------------------------------- |
| MongoDB           | ✅      | `bhiv_db` visible with logs        |
| FastAPI Backend   | ✅      | `/register` and `/agent` working   |
| Simulation Script | ✅      | 7 teams simulated successfully     |
| Dashboard         | ✅      | Visualization matches MongoDB data |
| N8N Workflows     | ✅      | Successfully tested via webhooks   |
| Test Coverage     | ✅      | 44.3% coverage with 60 tests passed  |

---

## 🎥 Suggested Demo Flow (for Video)

1. Start MongoDB and FastAPI
2. Show working `/register` and `/agent` in Swagger UI
3. Run simulation script
4. Show MongoDB Compass logs
5. Run Streamlit dashboard
6. Show N8N workflow import and testing
7. End with "System fully integrated with BHIV Core"

---

## 📚 Documentation

* [COMPLETE_PROJECT_GUIDE.md](./COMPLETE_PROJECT_GUIDE.md) — Full workflow explanation
* [docs/reflection.md](./docs/reflection.md) — Summary of implementation
* [docs/dashboard_verification.md](./docs/dashboard_verification.md) — Dashboard implementation details
* [docs/n8n_automation_proof.md](./docs/n8n_automation_proof.md) — N8N automation proof
* [docs/tests_coverage.md](./docs/tests_coverage.md) — Tests and coverage details
* [n8n/README.md](./n8n/README.md) — N8N workflow documentation
* [N8N Workflows Guide](./n8n/workflows/) — JSON automation files

---

## 🧠 Integration Notes

### BHIV Core Integration

This project is fully integrated with **Nisarg's BHIV Core System** through:

```
BHIV_CORE_URL=http://localhost:8002/reason
```

and tested with:

* Local FastAPI backend (port 8001)
* BHIV Core (port 8002)
* MongoDB (port 27017)

### Notes for Frontend Integration (Nikhil/Yash)

For frontend developers (Nikhil/Yash) integrating with this backend:

#### How to Consume APIs

1. **Team Registration Endpoint** (`/register`)
   - POST JSON payload with team details
   - Example payload:
     ```json
     {
       "team_name": "Frontend_Team",
       "members": ["Nikhil", "Yash"],
       "project_title": "Hackathon Dashboard"
     }
     ```

2. **Agent Interaction Endpoint** (`/agent`)
   - POST JSON payload with user query and optional context
   - Example payload:
     ```json
     {
       "user_input": "How to implement a dashboard?",
       "context": {
         "team_id": "frontend_team_123",
         "project_type": "web_application"
       }
     }
     ```

3. **Reward Endpoint** (`/reward`)
   - POST JSON payload with action and outcome for reward calculation
   - Example payload:
     ```json
     {
       "action": "step1 | step2 | step3",
       "outcome": "success"
     }
     ```

#### Shared Environment Variables

Use the following environment variables for consistency:
- `BHIV_CORE_URL`: Backend API base URL (https://ai-agent-x2iw.onrender.com)
- For local development, ensure your frontend can access the backend on the same network

#### Handling API Responses

1. **Success Responses**: Parse JSON responses containing `action`, `result`, and `reward` fields
2. **Error Responses**: Handle HTTP status codes (422 for validation errors, 500 for server errors)
3. **UI Updates**: Display agent responses in a conversational UI with clear separation of:
   - User input
   - Agent thoughts/planning
   - Executed actions
   - Results
   - Reward feedback

#### Example Implementation

For a dashboard view showing team logs:
- Poll the `/logs` endpoint periodically to get updated logs
- Display logs in a timeline view with team names and timestamps
- Use the `/reward` endpoint to submit outcomes and get reward feedback

---

## Client-Side Examples (e.g., for Frontend Integration)

To help frontend developers integrate more easily, here are JavaScript examples using the fetch API:

### Example for /register endpoint

```javascript
// JavaScript Fetch Example for /register
fetch('https://ai-agent-x2iw.onrender.com/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    team_name: 'Test_Team',
    members: ['Sejal', 'Akshay', 'Prajakta'],
    project_title: 'Smart AI Project'
  })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

### Example for /agent endpoint

```javascript
// JavaScript Fetch Example for /agent
fetch('https://ai-agent-x2iw.onrender.com/agent', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_input: 'Explain how to build a REST API with FastAPI',
    context: { team_id: 'demo_team', project_type: 'web_application' }
  })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

### Example for /reward endpoint

```javascript
// JavaScript Fetch Example for /reward
fetch('https://ai-agent-x2iw.onrender.com/reward', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    action: 'step1 | step2 | step3',
    outcome: 'success'
  })
})
.then(response => response.json())
.then(data => console.log('Reward:', data))
.catch(error => console.error('Error:', error));
```

### CORS Considerations

When developing locally, ensure your frontend domain is allowed in backend CORS settings if needed. The backend is configured to accept requests from common development origins.

---

## 👩‍💻 Author

**Sejal Dongre**
AI & Data Science Department
Hackathon Project — *BHIV Intelligent System Integration*

# ✅ Hackathon Backend — Final Submission (Sejal Dongre)

**Status:** All tests passing | **Coverage:** 83% | **Deployed:** [https://ai-agent-x2iw.onrender.com](https://ai-agent-x2iw.onrender.com)

## Verification Summary
- ✅ FastAPI + OpenAPI complete
- ✅ Storage & Transactions implemented
- ✅ N8N Automation verified
- ✅ Render deployment active
- ✅ CI/CD passing
- ✅ 44.3% test coverage

# HackaVerse Backend v2.0

## 🚀 Production-Ready Hackathon Engine

This repository contains the backend for HackaVerse, a production-ready hackathon management system with AI-powered agent processing, reward calculation, and comprehensive logging.

## 🎯 Key Features

### ✅ Modular Architecture
- **Core Connector**: BHIV Core integration (`src/core_connector.py`)
- **Bucket Connector**: Data and log relay (`src/bucket_connector.py`)
- **MCP Router**: Internal agent coordination (`src/mcp_router.py`)
- **Structured Logging**: KSML-compliant logging system (`src/logger.py`)

### ✅ API Endpoints
- **Agent Processing**: `POST /agent/`
- **Reward System**: `POST /admin/reward`
- **Team Registration**: `POST /admin/register`
- **N8N Webhook**: `POST /admin/webhook/hackaverse/registration`
- **System Health**: `GET /system/health`

### ✅ Automation Ready
- **N8N Workflows**: Pre-configured automation workflows
- **Webhook Endpoints**: For external system integration
- **Structured Logging**: For monitoring and debugging

## 📁 Repository Structure

```
.
├── src/                      # Backend source code
│   ├── core_connector.py     # BHIV Core integration
│   ├── bucket_connector.py   # Data/log relay to MongoDB
│   ├── mcp_router.py         # Agent coordination
│   ├── logger.py             # KSML logging utility
│   ├── models.py             # Data models
│   └── routes/               # API route handlers
├── n8n/                      # Automation workflows
│   ├── README.md             # Workflow documentation
│   └── workflows/            # JSON workflow definitions
├── API_REFERENCE.md          # Complete API documentation
├── INTEGRATION_NOTES.md      # Integration guidelines
├── QA_REPORT.md              # Quality assurance report
├── sample_logs.json          # KSML log examples
└── render.yaml              # Deployment configuration
```

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload --port 8001

# Visit http://127.0.0.1:8001/docs for API documentation
```

### Production Deployment
The backend is deployed on Render at: https://ai-agent-x2iw.onrender.com

## 📖 Documentation

- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Integration Guide**: [INTEGRATION_NOTES.md](INTEGRATION_NOTES.md)
- **Quality Assurance**: [QA_REPORT.md](QA_REPORT.md)
- **N8N Workflows**: [n8n/README.md](n8n/README.md)

## 🧪 Testing

- **Endpoint Validation**: [test_backend.py](test_backend.py)
- **System Verification**: [final_verification.py](final_verification.py)
- **Log Samples**: [sample_logs.json](sample_logs.json)

## 🤝 Handoff Information

### For Vinayak (QA & Task Bank)
- Comprehensive QA report in [QA_REPORT.md](QA_REPORT.md)
- Sample KSML logs in [sample_logs.json](sample_logs.json)
- Automated validation scripts
- N8N workflows for automation

### For Yash (Frontend Integration)
- Complete API documentation in [API_REFERENCE.md](API_REFERENCE.md)
- Integration examples in [INTEGRATION_NOTES.md](INTEGRATION_NOTES.md)
- Key endpoints ready for frontend consumption

### For BHIV Core Team
- Core connector in [src/core_connector.py](src/core_connector.py)
- Configurable via `BHIV_CORE_URL` environment variable

## 📋 Task Completion Summary

All requirements from the task description have been implemented:

1. ✅ **System Modularization** - Clean module structure with clear interfaces
2. ✅ **Connector Readiness** - Production-ready connectors with mock URLs
3. ✅ **API Endpoint Finalization** - All required endpoints implemented and documented
4. ✅ **Micro Flow Logging** - KSML-compliant structured logging
5. ✅ **N8N Workflow Hook** - Registration webhook with test payload
6. ✅ **Deployment & Testing** - Render deployment with documentation and samples

## 📞 Contact

For questions about this implementation:
- **Sejal**: [sejal@example.com]
- **Repository**: https://github.com/Sejal060/hackathon.git

---
**Status**: ✅ READY FOR HANDOFF  
**Version**: v2.0  
**Last Updated**: 2025-11-10