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