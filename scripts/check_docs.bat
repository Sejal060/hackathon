@echo off
echo Starting server...
start /b uvicorn src.main:app --reload --port 8000
timeout /t 2 /nobreak >nul
curl -s http://127.0.0.1:8000/openapi.json | jq ".info.title"
taskkill /f /im uvicorn.exe