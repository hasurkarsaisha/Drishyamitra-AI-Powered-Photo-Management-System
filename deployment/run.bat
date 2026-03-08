@echo off
echo Starting Drishyamitra...
echo.

echo Checking environment files...
if not exist backend\.env (
    echo Creating backend .env from example...
    copy backend\.env.example backend\.env
)

if not exist frontend\.env (
    echo Creating frontend .env from example...
    copy frontend\.env.example frontend\.env
)

echo.
echo Choose installation method:
echo 1. Docker (Recommended)
echo 2. Manual Setup
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting with Docker...
    docker-compose up --build
) else if "%choice%"=="2" (
    echo.
    echo Starting manual setup...
    echo.
    echo Starting Backend...
    start cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python app.py"
    
    timeout /t 5
    
    echo Starting Frontend...
    start cmd /k "cd frontend && npm install && npm run dev"
    
    echo.
    echo Services starting...
    echo Backend: http://localhost:5000
    echo Frontend: http://localhost:3000
) else (
    echo Invalid choice
    pause
)
