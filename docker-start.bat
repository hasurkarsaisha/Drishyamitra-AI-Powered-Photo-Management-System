@echo off
echo ========================================
echo   Drishyamitra - Docker Setup
echo ========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running!
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo Docker is installed ✓
echo.

echo Starting services with Docker Compose...
echo This will:
echo   - Start PostgreSQL database
echo   - Build and start backend (Python/Flask)
echo   - Build and start frontend (React/Vite)
echo.

docker-compose up --build

echo.
echo Services stopped.
pause
