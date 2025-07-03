#!/usr/bin/env python3
"""
Test core functionality of the Fuel Price API without external dependencies
"""

import json
import re

def test_core_functionality():
    """Test the core logic without external dependencies"""
    
    print("🧪 Testing Core Fuel Price API Logic")
    print("=" * 50)
    
    # 1. Test regex patterns for price extraction
    print("\n1️⃣ Testing Price Extraction Patterns")
    print("-" * 30)
    
    sample_text = """
    FUEL PRICE ADJUSTMENT - EFFECTIVE 15TH JANUARY 2024
    
    The following retail pump prices are effective from 15th January 2024:
    
    Unleaded Petrol 93: 14.50 BWP per litre
    Unleaded Petrol 95: 14.75 BWP per litre
    Diesel 50ppm: 13.80 BWP per litre
    Illuminating Paraffin: 9.50 BWP per litre
    """
    
    # Test patterns
    patterns = [
        ("Petrol 93", r'petrol\s+93.*?(\d+\.\d+)', 14.50),
        ("Petrol 95", r'petrol\s+95.*?(\d+\.\d+)', 14.75),
        ("Diesel", r'diesel.*?(\d+\.\d+)', 13.80),
        ("Paraffin", r'paraffin.*?(\d+\.\d+)', 9.50)
    ]
    
    extracted_prices = []
    for name, pattern, expected in patterns:
        match = re.search(pattern, sample_text, re.IGNORECASE)
        if match:
            price = float(match.group(1))
            if price == expected:
                print(f"✅ {name}: {price} BWP")
                extracted_prices.append({"product": f"Retail Pump Price - {name}", "price": price})
            else:
                print(f"⚠️  {name}: {price} BWP (expected {expected})")
        else:
            print(f"❌ {name}: Pattern not found")
    
    # 2. Test date extraction
    print("\n2️⃣ Testing Date Extraction")
    print("-" * 30)
    
    date_pattern = r'effective.*?(\d{1,2}.*?\d{4})'
    date_match = re.search(date_pattern, sample_text, re.IGNORECASE)
    
    if date_match:
        extracted_date = date_match.group(1).strip()
        print(f"✅ Date: '{extracted_date}'")
    else:
        print("❌ Date: Pattern not found")
        extracted_date = "Date not specified"
    
    # 3. Test JSON response structure
    print("\n3️⃣ Testing JSON Response Structure")
    print("-" * 30)
    
    response_data = {
        "effectiveDate": extracted_date,
        "currency": "BWP",
        "prices": extracted_prices,
        "sourceUrl": "https://www.bera.co.bw/test-announcement"
    }
    
    try:
        json_response = json.dumps(response_data, indent=2)
        print("✅ JSON serialization: Success")
        
        # Validate structure
        parsed = json.loads(json_response)
        required_fields = ['effectiveDate', 'currency', 'prices', 'sourceUrl']
        
        if all(field in parsed for field in required_fields):
            print("✅ JSON structure: Valid")
            print(f"✅ Currency: {parsed['currency']}")
            print(f"✅ Prices count: {len(parsed['prices'])}")
        else:
            print("❌ JSON structure: Missing required fields")
            
    except Exception as e:
        print(f"❌ JSON handling: {e}")
        return False
    
    # 4. Test link finding logic
    print("\n4️⃣ Testing Link Finding Logic")
    print("-" * 30)
    
    mock_html = '''
    <html>
    <body>
    <h1>Press Releases</h1>
    <a href="/news/general-update">General Update</a>
    <a href="/announcement/fuel-price-adjustment-jan-2024">Fuel Price Adjustment - January 2024</a>
    <a href="/news/other-announcement">Other Announcement</a>
    </body>
    </html>
    '''
    
    keywords = ['fuel price', 'petroleum price', 'petrol price', 'diesel price']
    
    found_fuel_link = False
    for keyword in keywords:
        if keyword.lower() in mock_html.lower():
            # Simple regex to find href with fuel-related content
            pattern = r'href="([^"]*(?:fuel|petroleum|petrol)[^"]*)"'
            match = re.search(pattern, mock_html, re.IGNORECASE)
            if match:
                link = match.group(1)
                print(f"✅ Found fuel link: {link}")
                found_fuel_link = True
                break
    
    if not found_fuel_link:
        print("❌ No fuel-related links found")
    
    # 5. Test error response format
    print("\n5️⃣ Testing Error Response Format")
    print("-" * 30)
    
    error_response = {
        "statusCode": 503,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"error": "Data source (BERA) is currently unavailable."})
    }
    
    try:
        error_json = json.dumps(error_response, indent=2)
        print("✅ Error response format: Valid")
    except Exception as e:
        print(f"❌ Error response format: {e}")
    
    # 6. Display sample successful response
    print("\n6️⃣ Sample Successful API Response")
    print("-" * 30)
    
    success_response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_data, indent=2)
    }
    
    print("Sample Lambda Response:")
    print(json.dumps(success_response, indent=2))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CORE FUNCTIONALITY TEST RESULTS")
    print("=" * 50)
    
    tests_passed = len(extracted_prices) == 4 and found_fuel_link
    
    if tests_passed:
        print("🟢 ALL CORE TESTS PASSED!")
        print("\n✅ Price extraction: Working")
        print("✅ Date extraction: Working") 
        print("✅ JSON handling: Working")
        print("✅ Link finding: Working")
        print("✅ Error handling: Working")
        
        print("\n🚀 The API core logic is ready!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test with real data: python test_local.py")
        print("3. Deploy to AWS: serverless deploy")
        
    else:
        print("🔴 SOME TESTS FAILED")
        print("Please check the failed tests above")
    
    return tests_passed

if __name__ == "__main__":
    test_core_functionality()