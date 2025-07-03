@echo off
echo 🔧 Fixing PowerShell and Running Botswana Fuel Price API Tests
echo ==============================================================
echo.

echo Step 1: Fix PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo.
echo Step 2: Check current directory and files...
python check_directory.py

echo.
echo Step 3: Install dependencies...
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2

echo.
echo Step 4: Test core functionality...
python test_core.py

echo.
echo Step 5: Test with real BERA data...
python test_real_bera.py

echo.
echo ==============================================================
echo 🎉 All tests completed!
echo ==============================================================
pause