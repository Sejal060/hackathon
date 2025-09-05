# src/main.py
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sejal's AI Agent System")

@app.get("/ping")
def ping():
    logger.info("Health check endpoint called")
    return {"message": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from dotenv import load_dotenv
import os
load_dotenv()  # Load from .env
api_key = os.getenv("GROQ_API_KEY")
from .agent import BasicAgent
from fastapi import Query

agent = BasicAgent(api_key="your-openai-key")  # Add to .env or secrets

@app.get("/agent")
def run_agent(input: str = Query(...)):
    return agent.process_input(input)