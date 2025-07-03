@echo off
echo 🧪 Running Complete Test Suite for Botswana Fuel Price API
echo ============================================================
echo.

echo Step 1: Installing dependencies...
pip install requests==2.31.0 beautifulsoup4==4.12.2

echo.
echo Step 2: Running core tests...
python test_core.py

echo.
echo Step 3: Running real BERA tests...
python test_real_bera.py

echo.
echo Step 4: Running comprehensive tests...
python test_comprehensive.py

echo.
echo ============================================================
echo 🎉 All tests completed!
echo.
echo If all tests passed, you can now:
echo 1. Deploy: serverless deploy
echo 2. Review BERA documentation: BERA_DOCUMENTATION.md
echo.
pause