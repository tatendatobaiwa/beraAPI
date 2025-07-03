@echo off
echo Installing dependencies for Botswana Fuel Price API...
echo.

echo Installing requests...
pip install requests==2.31.0

echo Installing beautifulsoup4...
pip install beautifulsoup4==4.12.2

echo.
echo Dependencies installed successfully!
echo.
echo You can now run:
echo   python test_local.py
echo   python test_comprehensive.py
echo.
pause