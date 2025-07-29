@echo off
REM Script to run Django application locally with PostgreSQL on Windows

echo Starting Django application with local PostgreSQL...

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from env.sample...
    copy env.sample .env
    echo Please edit .env file with your database credentials!
    pause
    exit /b 1
)

REM Load environment variables from .env file
for /f "delims=" %%x in (.env) do (
    set "line=%%x"
    setlocal enabledelayedexpansion
    set "line=!line:#=!"
    if not "!line!"=="" set "%%x"
    endlocal
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements
echo Checking Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Start the development server
echo Starting Django development server...
python manage.py runserver