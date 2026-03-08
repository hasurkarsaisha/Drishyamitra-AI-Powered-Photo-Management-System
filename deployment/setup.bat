@echo off
cd /d "%~dp0"
echo ========================================
echo   Drishyamitra - Initial Setup
echo ========================================
echo.
echo Working directory: %CD%
echo.

REM Check if .env files exist
echo [1/5] Checking environment files...
if not exist "backend\.env" (
    echo Creating backend\.env from example...
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env"
        echo Please edit backend\.env and add your API keys!
    ) else (
        echo ERROR: backend\.env.example not found!
    )
    echo.
)

if not exist "frontend\.env" (
    echo Creating frontend\.env from example...
    if exist "frontend\.env.example" (
        copy "frontend\.env.example" "frontend\.env"
    ) else (
        echo ERROR: frontend\.env.example not found!
    )
    echo.
)

REM Check PostgreSQL service
echo [2/5] Checking PostgreSQL service...
sc query postgresql-x64-18 | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo PostgreSQL is already running
) else (
    echo PostgreSQL is not running
    echo.
    echo IMPORTANT: You need to start PostgreSQL service
    echo Run this command as Administrator:
    echo   Start-Service postgresql-x64-18
    echo.
    echo OR manually start it:
    echo   D:\Postgres\bin\pg_ctl.exe start -D "D:\Postgres\data"
    echo.
    set /p continue="Press Enter after starting PostgreSQL, or Ctrl+C to exit..."
)

REM Setup database
echo.
echo [3/5] Setting up PostgreSQL database...
if exist "setup_postgres.py" (
    python setup_postgres.py
) else (
    echo ERROR: setup_postgres.py not found in %CD%
    set errorlevel=1
)
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Database setup failed!
    echo Make sure PostgreSQL is running and credentials are correct.
    pause
    exit /b 1
)

REM Install backend dependencies
echo.
echo [4/5] Installing backend dependencies...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
cd ..

REM Install frontend dependencies
echo.
echo [5/5] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit backend\.env and add your API keys (if not done)
echo   2. Run: start.bat
echo.
pause
