#!/bin/bash

echo "Starting development environment..."

# Start Chroma vector database
echo "Starting Chroma..."
cd chroma && ./startup.sh &

# Start FastAPI backend
echo "Starting FastAPI backend..."
cd ../backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Start React frontend
echo "Starting React frontend..."
cd ../frontend && npm run dev &

echo "All services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop all services"

wait
