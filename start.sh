#!/bin/bash

# Check if tmux is installed
if ! command -v tmux >/dev/null 2>&1; then
    echo "Error: tmux is not installed. Please install it first:"
    echo "sudo apt-get update && sudo apt-get install tmux"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "Error: docker-compose is not installed. Please install it first:"
    echo "sudo apt-get update && sudo apt-get install docker-compose"
    exit 1
fi

# Kill any existing godseye session
tmux kill-session -t godseye 2>/dev/null

# Create a new tmux session
tmux new-session -d -s godseye

# Split the window into four panes
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux split-window -v

# Start the FastAPI backend server in the first pane
tmux send-keys -t godseye:0.0 "cd backend && python3 main.py server" C-m

# Start the YCombinator scraper in the second pane
tmux send-keys -t godseye:0.1 "cd backend && python3 main.py yc-scraper --periodic --interval 24" C-m

# Start the frontend in the third pane
tmux send-keys -t godseye:0.2 "cd frontend && npm run dev" C-m

# Start Docker Compose in the fourth pane
tmux send-keys -t godseye:0.3 "docker-compose up" C-m

echo "==============================================="
echo "All components started in tmux session 'godseye'"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Scraper: Running in periodic mode every 24 hours"
echo "Docker services: Running via docker-compose"
echo "==============================================="
echo ""
echo "Tmux Session Commands:"
echo "  - Ctrl+b d: Detach from session"
echo "  - Ctrl+b arrow keys: Navigate between panes"
echo "  - Ctrl+b [: Enter scroll mode (use arrow keys to scroll, q to quit)"
echo ""
echo "To stop all components:"
echo "1. Press Ctrl+b then type :kill-session"
echo "2. Or run: tmux kill-session -t godseye"
echo ""
echo "To stop Docker services separately:"
echo "1. Navigate to Docker pane (Ctrl+b then arrow keys)"
echo "2. Press Ctrl+c to stop docker-compose"
echo "3. Or run: docker-compose down"
echo "==============================================="

# Attach to the tmux session
tmux attach-session -t godseye 