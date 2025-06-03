#!/bin/bash
cd backend || exit
port=5003
kill -9 $(lsof -ti tcp:$port) 2>/dev/null
source ../venv/bin/activate
uvicorn app:app --reload --port $port
