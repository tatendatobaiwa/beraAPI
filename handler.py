import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
BERA_URL = "https://www.bera.co.bw/media/press-releases"
TIMEOUT = 15

def get_prices(event, context):
    """Main Lambda function to get Botswana fuel prices"""
    try:
        # 1. Get press releases page
        html = fetch_page(BERA_URL)
        if not html:
            return error_response(503, "Data source (BERA) is currently unavailable.")
        
        # 2. Find fuel price announcement link
        announcement_url = find_fuel_announcement(html)
        if not announcement_url:
            return error_response(500, "Failed to parse data from the source. The scraper may need an update.")
        
        # 3. Get announcement page
        announcement_html = fetch_page(announcement_url)
        if not announcement_html:
            return error_response(503, "Data source (BERA) is currently unavailable.")
        
        # 4. Extract fuel data
        fuel_data = extract_prices(announcement_html, announcement_url)
        if not fuel_data:
            return error_response(500, "Failed to parse data from the source. The scraper may need an update.")
        
        # 5. Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(fuel_data)
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return error_response(500, "Failed to parse data from the source. The scraper may need an update.")

def fetch_page(url):
    """Fetch webpage content"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; FuelPriceBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except:
        return None

def find_fuel_announcement(html):
    """Find the latest fuel price announcement link"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for links with fuel-related keywords
        keywords = ['fuel price', 'petroleum price', 'petrol price', 'diesel price']
        
        for link in soup.find_all('a', href=True):
            text = link.get_text().lower()
            if any(keyword in text for keyword in keywords):
                href = link['href']
                # Convert relative URL to absolute
                if href.startswith('/'):
                    return urljoin(BERA_URL, href)
                return href
        
        return None
    except:
        return None

def extract_prices(html, source_url):
    """Extract fuel prices from announcement page"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        # Extract date
        date_match = re.search(r'effective.*?(\d{1,2}.*?\d{4})', text, re.IGNORECASE)
        effective_date = date_match.group(1) if date_match else "Date not specified"
        
        # Extract prices for each fuel type
        fuel_types = [
            ("Retail Pump Price - Unleaded Petrol 93", r'petrol\s+93.*?(\d+\.\d+)'),
            ("Retail Pump Price - Unleaded Petrol 95", r'petrol\s+95.*?(\d+\.\d+)'),
            ("Retail Pump Price - Diesel 50ppm", r'diesel.*?(\d+\.\d+)'),
            ("Wholesale Price - Illuminating Paraffin", r'paraffin.*?(\d+\.\d+)')
        ]
        
        prices = []
        for product, pattern in fuel_types:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    price = float(match.group(1))
                    prices.append({"product": product, "price": price})
                except:
                    continue
        
        if not prices:
            return None
        
        return {
            "effectiveDate": effective_date,
            "currency": "BWP",
            "prices": prices,
            "sourceUrl": source_url
        }
        
    except:
        return None

def error_response(status_code, message):
    """Create error response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"error": message})
    }