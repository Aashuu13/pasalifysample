@echo off
title Pasalify - Dev Server
color 1F

echo.
echo  ==========================================
echo       PASALIFY — Starting Dev Server
echo  ==========================================
echo.

:: Navigate to project folder
cd /d "C:\AI 39-B Group-1 Pasalifyy\pasalify"

:: Activate virtual environment
echo  [1/3] Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo  [2/3] Installing requirements...
python -m pip install -r requirements.txt

:: Run the app
echo  [3/3] Launching Flask app...
echo.
echo  ==========================================
echo    Server running at: http://127.0.0.1:5000
echo  ==========================================
echo.
python app.py

pause
