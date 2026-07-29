@echo off
echo ============================================
echo   AI Personal Assistant - Starting...
echo ============================================

REM Check if virtual environment exists
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Launch the app
echo Launching AI Assistant...
python main.py

pause
