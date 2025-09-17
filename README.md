# 🚀 Sejal Hackathon – 7-Day Production Sprint

This repository documents my **7-Day Hackathon Sprint**, where I designed, built, and deployed an AI-powered application while following best practices in software engineering and production deployment.  

The sprint was structured into **daily goals (MVPs)**, learning outcomes, and values such as humility, gratitude, and honesty.

---

## 📅 Sprint Plan

### **Day 1 – Foundation & Repo Setup**
- **Learning**:  
  - Repo best practices (`README`, `requirements.txt`).  
  - Basics of **FastAPI** / **Streamlit** for deployment.  
  - Production app structure (`src/`, `tests/`, `docs/`).  
- **Values**: Humility, Gratitude.  
- **Daily MVP**:  
  - Clean repo structure.  
  - Initial README with deployment target.  

---

### **Day 2 – Core Agent Loop**
- **Learning**:  
  - AI Agent basics (loop: input → reasoning → output).  
  - Importance of logging.  
- **Values**: Honesty.  
- **Daily MVP**:  
  - Script where agent takes input → returns structured JSON.  
  - Logs every step.  

---

### **Day 3 – Multi-Agent & RL Basics**
- **Learning**:  
  - Multi-agent systems (Planner vs Executor).  
  - Basics of Reinforcement Learning (RL).  
  - Reward simulation.  
- **Values**: Humility.  
- **Daily MVP**:  
  - Planner & Executor agents exchanging messages.  
  - Simple reward mechanism logged.  

---

### **Day 4 – MCPs & Modular Design**
- **Learning**:  
  - Modular Component Protocols (MCPs).  
  - Why modular design = stability in production.  
- **Values**: Gratitude.  
- **Daily MVP**:  
  - Code refactored into modules (`input_handler.py`, `reasoning.py`, `executor.py`, `reward.py`).  
  - Integration documented.  

---

### **Day 5 – Deployment to Production**
- **Learning**:  
  - Deployment on Render/Heroku/Streamlit Cloud.  
  - CI/CD with GitHub Actions.  
- **Values**: Honesty.  
- **Daily MVP**:  
  - Live public demo URL.  
  - Auto-deploy workflow configured.  

---

### **Day 6 – Testing & Outreach**
- **Learning**:  
  - Writing automated tests (pytest).  
  - Collecting peer feedback.  
- **Values**: Humility, Gratitude.  
- **Daily MVP**:  
  - 3–5 automated tests.  
  - `feedback.md` with outreach notes.  

---

### **Day 7 – Reflection & Showcase Prep**
- **Learning**:  
  - Documenting for reviewers.  
  - Value of reflection in growth.  
- **Values**: Honesty, Gratitude.  
- **Daily MVP**:  
  - Reflection (200–500 words).  
  - Demo video (2–3 mins).  
  - Final repo tag: `day7-production`.  

---

## 📦 Final Deliverables
1. Public repo (tag: `day7-production`).  
2. Working demo link.  
3. Demo video (2–3 minutes).  
4. Reflection (200–500 words).  
5. `feedback.md` (peer outreach notes).  
6. README with run/deploy instructions.  

---

## ⚡ Getting Started

### **Setup**
```bash
git clone https://github.com/Sejal060/hackathon.git
cd hackathon
pip install -r requirements.txt

**Working demo link**: [Live API Demo](https://ai-agent-x2iw.onrender.com/docs) (FastAPI on Render.com – test endpoints interactively!).
   - Root: https://ai-agent-x2iw.onrender.com/
   - Health check: https://ai-agent-x2iw.onrender.com/ping

   ## 🧪 Quick Test Guide (What to Evaluate)
1. Visit [Live Demo](https://ai-agent-x2iw.onrender.com/docs).
2. Test **/ping**: Should return `{"status": "ok"}`.
3. Test **/agent** (GET): Query `?input=Plan a hackathon trip` – expect JSON with `processed_input`, `action`, `result`, `reward`.
4. Test **/multi-agent** (GET): Query `?task=Build an AI agent` – expect `plan`, `result`, `reward`.
5. Edge case: Invalid input (e.g., empty `input=`) – should handle gracefully (no crash, returns error dict).
6. Check logs in Render dashboard for any issues.

Expected: <3s responses, modular flow (input → reasoning → execution → reward).