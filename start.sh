#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI backend..."
python backend/app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Streamlit frontend on port 5000
echo "Starting Streamlit frontend on port 5000..."
streamlit run frontend/streamlit_app.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true

# If streamlit exits, kill the backend too
kill $BACKEND_PID 2>/dev/null
