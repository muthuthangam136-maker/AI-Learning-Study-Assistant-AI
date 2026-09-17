@echo off
title AI Learning Assistant - Master Launcher
echo ====================================================
echo  LAUNCHING AI LEARNING & STUDY ASSISTANT (FULL-STACK)
echo ====================================================

echo [1/2] Launching Backend Server in a new window...
start "Backend - AI Learning Assistant" cmd /k "%~dp0start-backend.bat"

echo [2/2] Launching Frontend Web App in a new window...
start "Frontend - AI Learning Assistant" cmd /k "%~dp0start-frontend.bat"

echo.
echo Both servers are launching!
echo Backend will be available at:  http://localhost:8001
echo Swagger API Docs at:           http://localhost:8001/docs
echo Frontend will be available at: http://localhost:5173
echo ====================================================
