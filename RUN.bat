@echo off
title Water Quality Classification

cd /d "%~dp0"

echo    WATER QUALITY CLASSIFICATION

if not exist ".venv" (
    echo Creating Python environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Checking dependencies...
pip install -r requirements.txt

echo.
echo Starting application...
python start.py

pause