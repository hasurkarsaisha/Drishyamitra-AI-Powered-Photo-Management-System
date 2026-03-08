@echo off
echo ========================================
echo   Starting PostgreSQL Service
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Starting PostgreSQL service...
net start postgresql-x64-18

if %errorlevel% equ 0 (
    echo.
    echo ✅ PostgreSQL started successfully!
    echo.
    echo You can now run: setup.bat
) else (
    echo.
    echo ❌ Failed to start PostgreSQL
    echo.
    echo Try manually:
    echo   D:\Postgres\bin\pg_ctl.exe start -D "D:\Postgres\data"
)

echo.
pause
