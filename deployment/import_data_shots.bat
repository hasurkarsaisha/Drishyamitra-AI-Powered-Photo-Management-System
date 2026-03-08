@echo off
echo.
echo ========================================
echo   Import Photos from data-shots
echo ========================================
echo.
echo Found folder: D:\Drishyamitra\data-shots
echo.
echo This will import all photos to your account.
echo You'll need to enter your username and password.
echo.
pause
echo.

cd backend
python bulk_import.py "D:\Drishyamitra\data-shots"

echo.
echo ========================================
echo   Import Complete!
echo ========================================
echo.
echo Open http://localhost:3000/gallery to see your photos!
echo.
pause
