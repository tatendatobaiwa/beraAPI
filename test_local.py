#!/usr/bin/env python3
"""
Simple test script to test the fuel price scraper locally
"""

from handler import get_prices

def test_locally():
    """Test the get_prices function locally"""
    print("Testing Botswana Fuel Price API locally...")
    print("-" * 50)
    
    # Simulate Lambda event and context
    event = {}
    context = {}
    
    try:
        result = get_prices(event, context)
        
        print(f"Status Code: {result['statusCode']}")
        print(f"Response Body: {result['body']}")
        
        if result['statusCode'] == 200:
            print("\n✅ SUCCESS: API returned fuel prices!")
        else:
            print("\n❌ ERROR: API returned an error")
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")

if __name__ == "__main__":
    test_locally()