@echo off
chcp 65001 >nul
title VayuCoupler - MoES Coupled Air Quality Forecasting System
cls

echo ==============================================================================
echo        VayuCoupler - MoES Air Pollution-Weather Coupled Forecaster
echo          SIH26082: Smart India Hackathon - Ministry of Earth Sciences
echo ==============================================================================
echo.

cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Python was not detected on your Windows PC.
        echo [*] No problem! Launching VayuCoupler Standalone Desktop App directly...
        echo.
        timeout /t 2 >nul
        start "" msedge --app="%~dp0VayuCoupler_Windows_Offline_App.html" 2>nul || start "" chrome --app="%~dp0VayuCoupler_Windows_Offline_App.html" 2>nul || start "" "%~dp0VayuCoupler_Windows_Offline_App.html"
        exit /b 0
    ) else (
        set PY_CMD=py
    )
) else (
    set PY_CMD=python
)

echo [*] Python detected: %PY_CMD%
echo [*] Checking dependencies...

:: Create virtual environment if not present
if not exist "venv_win\Scripts\activate.bat" (
    echo [*] Setting up isolated Windows environment (venv_win)...
    %PY_CMD% -m venv venv_win
    call venv_win\Scripts\activate.bat
    echo [*] Installing required packages (FastAPI, Uvicorn, NumPy, Pandas)...
    pip install -q fastapi uvicorn numpy pandas
) else (
    call venv_win\Scripts\activate.bat
)

echo.
echo [*] Launching VayuCoupler High-Performance Backend Engine...
start /b python run.py >nul 2>&1

:: Wait 2 seconds for server startup
timeout /t 2 >nul

echo.
echo [OK] VayuCoupler is running live on http://127.0.0.1:8000
echo [*] Opening Native Desktop Window...
echo.

:: Launch in Microsoft Edge App Mode (Built into every Windows 10/11) or Google Chrome
start "" msedge --app="http://127.0.0.1:8000" --window-size=1440,900 2>nul || start "" chrome --app="http://127.0.0.1:8000" --window-size=1440,900 2>nul || start "" "http://127.0.0.1:8000"

echo ==============================================================================
echo  VayuCoupler is running in background! Keep this terminal window open.
echo  To shut down, simply close this window.
echo ==============================================================================
pause
