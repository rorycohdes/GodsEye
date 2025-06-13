#!/bin/bash

# Start the FastAPI backend server
gnome-terminal -- bash -c "cd backend && python3 main.py server; exec bash"

# Start the YCombinator scraper (periodic mode)
gnome-terminal -- bash -c "cd backend && python3 main.py yc-scraper --periodic --interval 24; exec bash"

# Start the frontend (assuming it's a Node.js/React app)
gnome-terminal -- bash -c "cd frontend && npm start; exec bash"

echo "All components started in separate terminals"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Scraper: Running in periodic mode every 24 hours" 