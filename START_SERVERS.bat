@echo off
echo ========================================
echo Starting Nyaysetu Case Management System
echo ========================================
echo.

echo Starting PostgreSQL (if not already running)...
echo Please ensure PostgreSQL is running on port 5432
echo.

echo Starting Backend Server...
start "Nyaysetu Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload"
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Nyaysetu Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Servers Starting...
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Test Credentials:
echo   Citizen: citizen1@example.com / password123
echo   Judge: judge1@example.com / password123
echo.
echo Press any key to exit this window...
pause >nul
