@echo off
echo 🚀 Deploying Botswana Fuel Price API...
echo =======================================

REM Check if serverless is installed
where serverless >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Serverless Framework not found. Installing...
    npm install -g serverless
)

REM Install plugin
echo 📦 Installing Python requirements plugin...
serverless plugin install -n serverless-python-requirements

REM Deploy
echo 🚀 Deploying to AWS...
serverless deploy

echo.
echo ✅ Deployment complete!
echo.
echo 📋 To test your API:
echo    serverless invoke local -f getPrices
echo.
echo 🌐 Your API endpoint will be shown above
pause