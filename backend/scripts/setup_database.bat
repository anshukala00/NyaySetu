@echo off
REM Nyaysetu Database Setup Script for Windows
REM This script automates the PostgreSQL database initialization

echo ========================================
echo Nyaysetu Database Setup
echo ========================================
echo.

REM Check if psql is available
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PostgreSQL is not installed or not in PATH
    echo.
    echo Please install PostgreSQL first:
    echo 1. Download from: https://www.postgresql.org/download/windows/
    echo 2. Add to PATH: C:\Program Files\PostgreSQL\15\bin
    echo.
    pause
    exit /b 1
)

echo PostgreSQL found!
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

echo Running database initialization script...
echo You will be prompted for the postgres superuser password.
echo.

REM Run the SQL initialization script
psql -U postgres -f "%SCRIPT_DIR%init_db.sql"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Database setup completed.
    echo ========================================
    echo.
    echo Database: nyaysetu
    echo User: nyaysetu_user
    echo Password: nyaysetu_pass
    echo.
    echo Connection string:
    echo postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
    echo.
    echo Next steps:
    echo 1. Update backend/.env with the connection string
    echo 2. Run: python test_db_connection.py
    echo 3. Run: alembic upgrade head
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Database setup failed
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Verify PostgreSQL is running
    echo 2. Check if you entered the correct postgres password
    echo 3. Try running manually: psql -U postgres -f init_db.sql
    echo.
)

pause
