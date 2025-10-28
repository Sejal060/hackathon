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

### Test Coverage: **82.38%**

Tests are implemented for all core components:

* ✅ Storage Service (`tests/test_storage.py`)
* ✅ Transaction Manager (`tests/test_transaction_manager.py`)
* ✅ BHIV Connectors (`tests/test_bhiv_connectors.py`)
* ✅ API Endpoints (`tests/test_endpoints.py`)
* ✅ Reward System (`tests/test_reward.py`)
* ✅ Executor Module (`tests/test_executor.py`)
* ✅ Reasoning Module (`tests/test_reasoning.py`)
* ✅ Reinforcement Learning (`tests/test_rl.py`)

### Run Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=src

# Run tests with detailed coverage reports
pytest tests/ --cov=src --cov-report=html --cov-report=xml
```

### Test Results
```
===== 44 passed in 257.83s (0:04:17) ======
```

### Coverage Details
```
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
src\__init__.py                           0      0   100%
src\agent.py                             24     24     0%
src\executor.py                          33      6    82%
src\input_handler.py                      4      0   100%
src\integrations\__init__.py              0      0   100%
src\integrations\bhiv_connectors.py      43      2    95%
src\main.py                             116      8    93%
src\multi_agent.py                       17     17     0%
src\reasoning.py                         35      8    77%
src\reward.py                            41      4    90%
src\routes.py                            40      5    88%
src\schemas.py                           13      0   100%
src\storage_service.py                   64      9    86%
src\transaction_manager.py               58      3    95%
---------------------------------------------------------
TOTAL                                   488     86    82%
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

```bash
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
| Test Coverage     | ✅      | 82.38% coverage with 44 tests passed |

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

## 🧠 Integration Note

This project is fully integrated with **Nisarg's BHIV Core System** through:

```
BHIV_CORE_URL=http://localhost:8002/reason
```

and tested with:

* Local FastAPI backend (port 8001)
* BHIV Core (port 8002)
* MongoDB (port 27017)

---

## 👩‍💻 Author

**Sejal Dongre**
AI & Data Science Department
Hackathon Project — *BHIV Intelligent System Integration*