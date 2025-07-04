# Botswana Fuel Price API

A simple serverless API that gets the latest fuel prices for Botswana from the BERA website.

## What it does

- Scrapes fuel prices from BERA's press releases
- Returns data in clean JSON format
- Runs on AWS Lambda (serverless)

## API Endpoint

**GET** `/prices`

### Example Response

```json
{
  "effectiveDate": "15 July 2025",
  "currency": "BWP",
  "prices": [
    {
      "product": "Retail Pump Price - Unleaded Petrol 93",
      "price": 14.50
    },
    {
      "product": "Retail Pump Price - Unleaded Petrol 95",
      "price": 14.75
    },
    {
      "product": "Retail Pump Price - Diesel 50ppm",
      "price": 13.80
    },
    {
      "product": "Wholesale Price - Illuminating Paraffin",
      "price": 9.50
    }
  ],
  "sourceUrl": "https://www.bera.co.bw/path/to/announcement"
}
```

## Quick Start

1. **Install Serverless Framework**
   ```bash
   npm install -g serverless
   serverless plugin install -n serverless-python-requirements
   ```

2. **Configure AWS**
   ```bash
   aws configure
   ```

3. **Deploy**
   ```bash
   # Linux/Mac
   ./deploy.sh
   
   # Windows
   deploy.bat
   
   # Or manually
   serverless deploy
   ```

4. **Test the API**
   ```bash
   # Run all tests (Windows)
   test_all.bat
   
   # Or run individual tests
   python test_core.py          # Core functionality
   python test_real_bera.py     # Real BERA data
   python test_comprehensive.py # Full test suite
   
   # Or use the guided test runner
   python run_tests.py
   ```

## How it works

1. Fetches BERA press releases page
2. Finds the latest fuel price announcement
3. Extracts prices using simple regex patterns
4. Returns structured JSON data

## Dependencies

- `requests` - for HTTP requests
- `beautifulsoup4` - for HTML parsing

## Data Source

Scrapes from: https://www.bera.co.bw/media/press-releases#   b e r a A P I  
 