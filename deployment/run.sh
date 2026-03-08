#!/bin/bash

echo "Starting Drishyamitra..."
echo ""

echo "Checking environment files..."
if [ ! -f backend/.env ]; then
    echo "Creating backend .env from example..."
    cp backend/.env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend .env from example..."
    cp frontend/.env.example frontend/.env
fi

echo ""
echo "Choose installation method:"
echo "1. Docker (Recommended)"
echo "2. Manual Setup"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Starting with Docker..."
    docker-compose up --build
elif [ "$choice" = "2" ]; then
    echo ""
    echo "Starting manual setup..."
    echo ""
    
    echo "Starting Backend..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py &
    BACKEND_PID=$!
    cd ..
    
    sleep 5
    
    echo "Starting Frontend..."
    cd frontend
    npm install
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "Services started!"
    echo "Backend: http://localhost:5000 (PID: $BACKEND_PID)"
    echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
    wait
else
    echo "Invalid choice"
    exit 1
fi
