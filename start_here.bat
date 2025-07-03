@echo off
echo 🚀 Botswana Fuel Price API - Starting from beraAPI directory
echo ============================================================
echo.

echo Current directory:
cd

echo.
echo Checking if we're in the right directory...
if exist "handler.py" (
    echo ✅ Found handler.py - we're in the right place!
) else (
    echo ❌ handler.py not found. Let's navigate to beraAPI directory...
    if exist "beraAPI" (
        echo Found beraAPI directory, changing to it...
        cd beraAPI
    ) else (
        echo Please make sure you're running this from the directory containing beraAPI folder
        pause
        exit /b 1
    )
)

echo.
echo Current directory after navigation:
cd

echo.
echo Step 1: Fixing PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo.
echo Step 2: Installing dependencies...
pip install requests==2.31.0 beautifulsoup4==4.12.2

echo.
echo Step 3: Running tests...
echo.

echo Testing core functionality...
python test_core.py

echo.
echo Testing with real BERA data...
python test_real_bera.py

echo.
echo ============================================================
echo 🎉 Tests completed! Check results above.
echo ============================================================
pause