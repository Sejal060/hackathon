# 🧠 Sejal’s AI Hackathon System

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

---



## 🧾 Verification Summary

| Component         | Status | Verification                       |
| ----------------- | ------ | ---------------------------------- |
| MongoDB           | ✅      | `bhiv_db` visible with logs        |
| FastAPI Backend   | ✅      | `/register` and `/agent` working   |
| Simulation Script | ✅      | 7 teams simulated successfully     |
| Dashboard         | ✅      | Visualization matches MongoDB data |
| N8N Workflows     | ✅      | Successfully tested via webhooks   |

---

## 🎥 Suggested Demo Flow (for Video)

1. Start MongoDB and FastAPI
2. Show working `/register` and `/agent` in Swagger UI
3. Run simulation script
4. Show MongoDB Compass logs
5. Run Streamlit dashboard
6. (Optional) Trigger N8N workflow
7. End with "System fully integrated with BHIV Core"

---

## 📚 Documentation

* [COMPLETE_PROJECT_GUIDE.md](./COMPLETE_PROJECT_GUIDE.md) — Full workflow explanation
* [docs/reflection.md](./docs/reflection.md) — Summary of implementation
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