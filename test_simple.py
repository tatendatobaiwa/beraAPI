#!/usr/bin/env python3
"""
Simple test to check if our handler works without external dependencies
"""

import json
import re

def mock_requests_get(url, **kwargs):
    """Mock requests.get for testing"""
    class MockResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code
        
        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception(f"HTTP {self.status_code}")
    
    # Mock BERA press releases page
    if "press-releases" in url:
        mock_html = '''
        <html>
        <body>
        <a href="/announcement/fuel-price-adjustment-2024">Latest Fuel Price Adjustment - January 2024</a>
        <a href="/other-news">Other News</a>
        </body>
        </html>
        '''
        return MockResponse(mock_html)
    
    # Mock fuel price announcement page
    elif "announcement" in url:
        mock_announcement = '''
        <html>
        <body>
        <h1>Fuel Price Adjustment - Effective 15th January 2024</h1>
        <p>The following prices are effective from 15th January 2024:</p>
        <ul>
        <li>Unleaded Petrol 93: 14.50 BWP per litre</li>
        <li>Unleaded Petrol 95: 14.75 BWP per litre</li>
        <li>Diesel 50ppm: 13.80 BWP per litre</li>
        <li>Illuminating Paraffin: 9.50 BWP per litre</li>
        </ul>
        </body>
        </html>
        '''
        return MockResponse(mock_announcement)
    
    return MockResponse("Not found", 404)

def mock_beautifulsoup(html, parser):
    """Mock BeautifulSoup for testing"""
    class MockSoup:
        def __init__(self, html):
            self.html = html
        
        def find_all(self, tag, **kwargs):
            if tag == 'a':
                # Return mock links
                class MockLink:
                    def __init__(self, text, href):
                        self._text = text
                        self._href = href
                    
                    def get_text(self):
                        return self._text
                    
                    def __getitem__(self, key):
                        if key == 'href':
                            return self._href
                        return None
                
                if "press-releases" in self.html:
                    return [
                        MockLink("Latest Fuel Price Adjustment - January 2024", "/announcement/fuel-price-adjustment-2024"),
                        MockLink("Other News", "/other-news")
                    ]
            return []
        
        def get_text(self):
            # Extract text content for price parsing
            if "Effective" in self.html:
                return """
                Fuel Price Adjustment - Effective 15th January 2024
                The following prices are effective from 15th January 2024:
                Unleaded Petrol 93: 14.50 BWP per litre
                Unleaded Petrol 95: 14.75 BWP per litre
                Diesel 50ppm: 13.80 BWP per litre
                Illuminating Paraffin: 9.50 BWP per litre
                """
            return self.html
    
    return MockSoup(html)

def test_with_mocks():
    """Test the handler with mocked dependencies"""
    print("🧪 Testing Botswana Fuel Price API with mock data...")
    print("=" * 60)
    
    # Mock the imports
    import sys
    from unittest.mock import MagicMock
    
    # Create mock modules
    mock_requests = MagicMock()
    mock_requests.get = mock_requests_get
    
    mock_bs4 = MagicMock()
    mock_bs4.BeautifulSoup = mock_beautifulsoup
    
    # Mock urllib.parse.urljoin
    def mock_urljoin(base, url):
        if url.startswith('/'):
            return f"https://www.bera.co.bw{url}"
        return url
    
    mock_urllib = MagicMock()
    mock_urllib.parse = MagicMock()
    mock_urllib.parse.urljoin = mock_urljoin
    
    # Inject mocks
    sys.modules['requests'] = mock_requests
    sys.modules['bs4'] = mock_bs4
    sys.modules['urllib'] = mock_urllib
    sys.modules['urllib.parse'] = mock_urllib.parse
    
    # Now import and test our handler
    try:
        from handler import get_prices
        
        # Test the function
        event = {}
        context = {}
        
        result = get_prices(event, context)
        
        print(f"✅ Status Code: {result['statusCode']}")
        print(f"✅ Headers: {result['headers']}")
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            print(f"✅ Response Body:")
            print(json.dumps(body, indent=2))
            
            # Validate response structure
            required_fields = ['effectiveDate', 'currency', 'prices', 'sourceUrl']
            missing_fields = [field for field in required_fields if field not in body]
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ All required fields present")
                
            if body.get('currency') == 'BWP':
                print("✅ Currency is correct (BWP)")
            else:
                print(f"❌ Currency is incorrect: {body.get('currency')}")
                
            if len(body.get('prices', [])) > 0:
                print(f"✅ Found {len(body['prices'])} fuel prices")
                for price in body['prices']:
                    print(f"   - {price['product']}: {price['price']} BWP")
            else:
                print("❌ No prices found")
                
        else:
            print(f"❌ Error response: {result['body']}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_mocks()