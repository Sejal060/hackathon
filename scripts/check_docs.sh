#!/usr/bin/env bash
uvicorn src.main:app --reload --port 8000 &
sleep 2
curl -s http://127.0.0.1:8000/openapi.json | jq '.info.title'
pkill -f "uvicorn src.main:app"