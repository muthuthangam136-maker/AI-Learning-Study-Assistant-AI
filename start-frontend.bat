@echo off
title AI Learning Assistant - Frontend Web App
echo ====================================================
echo  STARTING AI LEARNING & STUDY ASSISTANT FRONTEND
echo ====================================================

cd /d "%~dp0frontend"

:: Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not found in PATH!
    echo Please install Node.js (LTS) from https://nodejs.org
    pause
    exit /b 1
)

:: Install npm packages if node_modules does not exist
if not exist "node_modules\" (
    echo [INFO] Installing frontend dependencies with npm...
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed.
        pause
        exit /b 1
    )
)

:: Start Vite Dev Server
echo [INFO] Starting Vite development server...
npm run dev

pause
