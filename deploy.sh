#!/bin/bash

# Simple deployment script for Botswana Fuel Price API

echo "🚀 Deploying Botswana Fuel Price API..."
echo "======================================="

# Check if serverless is installed
if ! command -v serverless &> /dev/null; then
    echo "❌ Serverless Framework not found. Installing..."
    npm install -g serverless
fi

# Check if plugin is installed
if ! serverless plugin list | grep -q "serverless-python-requirements"; then
    echo "📦 Installing Python requirements plugin..."
    serverless plugin install -n serverless-python-requirements
fi

# Deploy
echo "🚀 Deploying to AWS..."
serverless deploy

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 To test your API:"
echo "   serverless invoke local -f getPrices"
echo ""
echo "🌐 Your API endpoint will be shown above"