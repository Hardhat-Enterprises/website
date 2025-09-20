@echo off
echo Starting Django server with automatic image optimization...
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this from the website directory.
    pause
    exit /b 1
)

REM Run the server with optimization
python manage.py runserver_with_optimization

pause
