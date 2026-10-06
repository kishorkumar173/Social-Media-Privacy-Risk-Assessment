@echo off
echo ======================================================================
echo 🔒 Social Media Privacy Risk Assessment Framework
echo ======================================================================
echo.
echo [*] Checking Python installation...
python --version
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [*] Initializing database and synthetic dataset...
python data/generate_dataset.py

echo [*] Executing automated test suite...
python -m unittest tests/test_privacy_assessment.py

echo.
echo [*] Starting Flask Backend & Web Interface on http://127.0.0.1:5000 ...
python backend/app.py
pause
