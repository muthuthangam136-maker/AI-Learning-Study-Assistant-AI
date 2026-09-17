@echo off
title AI Learning Assistant - Backend Server
echo ====================================================
echo  STARTING AI LEARNING & STUDY ASSISTANT BACKEND
echo ====================================================

cd /d "%~dp0backend"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.10+ from https://python.org and check "Add Python to PATH".
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo [INFO] Verifying and installing requirements...
pip install -r requirements.txt

:: Check if .env exists
if not exist ".env" (
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env
)

:: Run RAG Ingestion if needed
echo [INFO] Running RAG ingestion to index knowledge documents...
python scripts\ingest.py

:: Start FastAPI Backend Server
echo [INFO] Starting FastAPI Uvicorn Server at http://localhost:8001 ...
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

pause
