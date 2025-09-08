# src/main.py
from fastapi import FastAPI, Query
from .agent import BasicAgent
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sejal's AI Agent System")

# Initialize the agent with API key from environment variables (or placeholder)
api_key = os.getenv("OPENAI_API_KEY", "your-openai-key")  # Fallback to placeholder
agent = BasicAgent(api_key=api_key)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "message": "FastAPI is running",
        "endpoints": ["/ping", "/agent", "/docs", "/redoc"],
        "docs": "http://127.0.0.1:8001/docs"
    }

@app.get("/ping")
def ping():
    logger.info("Health check endpoint called")
    return {"message": "pong"}

@app.get("/agent")
def run_agent(input: str = Query(...)):
    return agent.process_input(input)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)