# src/main.py
from fastapi import FastAPI, HTTPException
import logging
import os
from dotenv import load_dotenv

# Load environment variables (e.g., for future API keys)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sejal's AI Agent System")

@app.get("/ping")
def ping():
    try:
        logger.info("Health check endpoint called")
        return {"message": "pong", "status": "healthy", "timestamp": logging.getLogger().handlers[0].formatter.formatTime(logging.getLogger().handlers[0].formatter.converter()))
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")