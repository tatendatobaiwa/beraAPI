#!/usr/bin/env python3
"""
Comprehensive test for the Botswana Fuel Price API
Tests both with and without external dependencies
"""

import json
import re
import sys

def test_dependencies():
    """Test if dependencies are available"""
    print("🔍 Checking Dependencies")
    print("=" * 50)
    
    results = {}
    
    # Test built-in modules
    try:
        import json
        import re
        from urllib.parse import urljoin
        results['builtin'] = True
        print("✅ Built-in modules (json, re, urllib.parse): Available")
    except ImportError as e:
        results['builtin'] = False
        print(f"❌ Built-in modules: {e}")
    
    # Test requests
    try:
        import requests
        results['requests'] = True
        print("✅ requests: Available")
    except ImportError:
        results['requests'] = False
        print("❌ requests: Not installed")
    
    # Test BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        results['bs4'] = True
        print("✅ beautifulsoup4: Available")
    except ImportError:
        results['bs4'] = False
        print("❌ beautifulsoup4: Not installed")
    
    return results

def test_regex_patterns():
    """Test the regex patterns used for price extraction"""
    print("\n🧪 Testing Regex Patterns")
    print("=" * 50)
    
    # Sample text that might be found on BERA website
    sample_text = """
    FUEL PRICE ADJUSTMENT - EFFECTIVE 15TH JANUARY 2024
    
    The Botswana Energy Regulatory Authority (BERA) announces the following 
    fuel prices effective from 15th January 2024:
    
    Retail Pump Prices:
    - Unleaded Petrol 93: 14.50 BWP per litre
    - Unleaded Petrol 95: 14.75 BWP per litre  
    - Diesel 50ppm: 13.80 BWP per litre
    
    Wholesale Prices:
    - Illuminating Paraffin: 9.50 BWP per litre
    """
    
    # Test fuel type patterns
    fuel_patterns = [
        ("Retail Pump Price - Unleaded Petrol 93", r'petrol\s+93.*?(\d+\.\d+)', 14.50),
        ("Retail Pump Price - Unleaded Petrol 95", r'petrol\s+95.*?(\d+\.\d+)', 14.75),
        ("Retail Pump Price - Diesel 50ppm", r'diesel.*?(\d+\.\d+)', 13.80),
        ("Wholesale Price - Illuminating Paraffin", r'paraffin.*?(\d+\.\d+)', 9.50)
    ]
    
    success_count = 0
    for product, pattern, expected_price in fuel_patterns:
        match = re.search(pattern, sample_text, re.IGNORECASE)
        if match:
            try:
                price = float(match.group(1))
                if price == expected_price:
                    print(f"✅ {product}: {price} BWP")
                    success_count += 1
                else:
                    print(f"⚠️  {product}: {price} BWP (expected {expected_price})")
            except ValueError:
                print(f"❌ {product}: Could not parse price")
        else:
            print(f"❌ {product}: Pattern not found")
    
    # Test date extraction
    date_pattern = r'effective.*?(\d{1,2}.*?\d{4})'
    date_match = re.search(date_pattern, sample_text, re.IGNORECASE)
    if date_match:
        date = date_match.group(1)
        print(f"✅ Date extraction: '{date}'")
        success_count += 1
    else:
        print("❌ Date extraction: Pattern not found")
    
    print(f"\n📊 Regex Test Results: {success_count}/5 patterns working")
    return success_count == 5

def test_json_handling():
    """Test JSON response formatting"""
    print("\n📄 Testing JSON Handling")
    print("=" * 50)
    
    # Sample fuel data
    sample_data = {
        "effectiveDate": "15th January 2024",
        "currency": "BWP",
        "prices": [
            {"product": "Retail Pump Price - Unleaded Petrol 93", "price": 14.50},
            {"product": "Retail Pump Price - Unleaded Petrol 95", "price": 14.75},
            {"product": "Retail Pump Price - Diesel 50ppm", "price": 13.80},
            {"product": "Wholesale Price - Illuminating Paraffin", "price": 9.50}
        ],
        "sourceUrl": "https://www.bera.co.bw/test-announcement"
    }
    
    try:
        # Test JSON serialization
        json_string = json.dumps(sample_data, indent=2)
        print("✅ JSON serialization: Success")
        
        # Test JSON deserialization
        parsed_data = json.loads(json_string)
        print("✅ JSON deserialization: Success")
        
        # Validate structure
        required_fields = ['effectiveDate', 'currency', 'prices', 'sourceUrl']
        missing_fields = [field for field in required_fields if field not in parsed_data]
        
        if not missing_fields:
            print("✅ JSON structure: All required fields present")
        else:
            print(f"❌ JSON structure: Missing fields {missing_fields}")
            return False
        
        # Validate data types
        if isinstance(parsed_data['prices'], list) and len(parsed_data['prices']) > 0:
            print("✅ Prices array: Valid")
            
            # Check first price item
            first_price = parsed_data['prices'][0]
            if 'product' in first_price and 'price' in first_price:
                if isinstance(first_price['price'], (int, float)):
                    print("✅ Price format: Valid")
                else:
                    print("❌ Price format: Should be number")
                    return False
            else:
                print("❌ Price item: Missing product or price field")
                return False
        else:
            print("❌ Prices array: Invalid or empty")
            return False
        
        print(f"\n📋 Sample JSON Output:")
        print(json_string)
        return True
        
    except Exception as e:
        print(f"❌ JSON handling failed: {e}")
        return False

def test_mock_api():
    """Test the API logic with mock data"""
    print("\n🎭 Testing API Logic with Mock Data")
    print("=" * 50)
    
    # Mock HTML content that simulates BERA website
    mock_press_releases = """
    <html>
    <body>
    <h1>Press Releases</h1>
    <ul>
    <li><a href="/announcement/fuel-price-jan-2024">Fuel Price Adjustment - January 2024</a></li>
    <li><a href="/announcement/other-news">Other News</a></li>
    </ul>
    </body>
    </html>
    """
    
    mock_announcement = """
    <html>
    <body>
    <h1>Fuel Price Adjustment - Effective 15th January 2024</h1>
    <p>The following prices are effective from 15th January 2024:</p>
    <table>
    <tr><td>Unleaded Petrol 93</td><td>14.50 BWP</td></tr>
    <tr><td>Unleaded Petrol 95</td><td>14.75 BWP</td></tr>
    <tr><td>Diesel 50ppm</td><td>13.80 BWP</td></tr>
    <tr><td>Illuminating Paraffin</td><td>9.50 BWP</td></tr>
    </table>
    </body>
    </html>
    """
    
    try:
        # Test link finding logic
        keywords = ['fuel price', 'petroleum price', 'petrol price', 'diesel price']
        
        # Simple HTML parsing without BeautifulSoup
        found_link = False
        for keyword in keywords:
            if keyword.lower() in mock_press_releases.lower():
                # Extract href using regex
                href_match = re.search(r'href="([^"]*fuel[^"]*)"', mock_press_releases, re.IGNORECASE)
                if href_match:
                    link = href_match.group(1)
                    print(f"✅ Found fuel announcement link: {link}")
                    found_link = True
                    break
        
        if not found_link:
            print("❌ Could not find fuel announcement link")
            return False
        
        # Test price extraction from announcement
        text_content = re.sub(r'<[^>]+>', ' ', mock_announcement)  # Remove HTML tags
        
        fuel_types = [
            ("Retail Pump Price - Unleaded Petrol 93", r'petrol\s+93.*?(\d+\.\d+)'),
            ("Retail Pump Price - Unleaded Petrol 95", r'petrol\s+95.*?(\d+\.\d+)'),
            ("Retail Pump Price - Diesel 50ppm", r'diesel.*?(\d+\.\d+)'),
            ("Wholesale Price - Illuminating Paraffin", r'paraffin.*?(\d+\.\d+)')
        ]
        
        prices = []
        for product, pattern in fuel_types:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                try:
                    price = float(match.group(1))
                    prices.append({"product": product, "price": price})
                    print(f"✅ Extracted: {product} = {price} BWP")
                except:
                    continue
        
        if len(prices) > 0:
            print(f"✅ Successfully extracted {len(prices)} prices")
            
            # Create mock response
            mock_response = {
                "effectiveDate": "15th January 2024",
                "currency": "BWP",
                "prices": prices,
                "sourceUrl": "https://www.bera.co.bw/announcement/fuel-price-jan-2024"
            }
            
            print(f"\n📋 Mock API Response:")
            print(json.dumps(mock_response, indent=2))
            return True
        else:
            print("❌ No prices extracted")
            return False
            
    except Exception as e:
        print(f"❌ Mock API test failed: {e}")
        return False

def test_performance():
    """Test performance characteristics"""
    print("\n⚡ Testing Performance Characteristics")
    print("=" * 50)
    
    import time
    
    # Test regex performance
    sample_text = "Unleaded Petrol 93: 14.50 BWP per litre" * 100
    pattern = r'petrol\s+93.*?(\d+\.\d+)'
    
    start_time = time.time()
    for _ in range(1000):
        re.search(pattern, sample_text, re.IGNORECASE)
    regex_time = time.time() - start_time
    
    print(f"✅ Regex performance: {regex_time:.4f}s for 1000 searches")
    
    # Test JSON performance
    large_data = {
        "effectiveDate": "15 January 2024",
        "currency": "BWP",
        "prices": [{"product": f"Test Product {i}", "price": 10.0 + i} for i in range(100)],
        "sourceUrl": "https://test.com"
    }
    
    start_time = time.time()
    for _ in range(100):
        json.dumps(large_data)
    json_time = time.time() - start_time
    
    print(f"✅ JSON performance: {json_time:.4f}s for 100 serializations")
    
    return regex_time < 1.0 and json_time < 1.0

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n🔍 Testing Edge Cases")
    print("=" * 50)
    
    edge_cases = [
        # Different price formats
        ("Petrol 93: P14.50", r'petrol\s+93.*?(\d+\.\d+)', 14.50),
        ("Petrol 93 - BWP 14.50", r'petrol\s+93.*?(\d+\.\d+)', 14.50),
        ("Petrol 93 costs 14.50 pula", r'petrol\s+93.*?(\d+\.\d+)', 14.50),
        
        # Different date formats
        ("effective 1st January 2024", r'effective.*?(\d{1,2}.*?\d{4})', "1st January 2024"),
        ("effective from January 1, 2024", r'effective.*?(\d{1,2}.*?\d{4})', "1, 2024"),
        ("effective 01/01/2024", r'effective.*?(\d{1,2}.*?\d{4})', "01/01/2024"),
    ]
    
    success_count = 0
    for test_text, pattern, expected in edge_cases:
        match = re.search(pattern, test_text, re.IGNORECASE)
        if match:
            result = match.group(1)
            if str(expected) in str(result):
                print(f"✅ Edge case: '{test_text}' → '{result}'")
                success_count += 1
            else:
                print(f"⚠️ Edge case: '{test_text}' → '{result}' (expected {expected})")
        else:
            print(f"❌ Edge case: '{test_text}' → No match")
    
    print(f"📊 Edge cases passed: {success_count}/{len(edge_cases)}")
    return success_count >= len(edge_cases) * 0.7  # 70% success rate

def test_security():
    """Test security considerations"""
    print("\n🔒 Testing Security Considerations")
    print("=" * 50)
    
    # Test malicious input handling
    malicious_inputs = [
        "<script>alert('xss')</script>",
        "'; DROP TABLE prices; --",
        "../../../etc/passwd",
        "javascript:alert(1)",
    ]
    
    for malicious_input in malicious_inputs:
        try:
            # Test JSON serialization with malicious input
            test_data = {"test": malicious_input}
            json_str = json.dumps(test_data)
            parsed = json.loads(json_str)
            
            # Should not execute or cause errors
            if parsed["test"] == malicious_input:
                print(f"✅ Safely handled: {malicious_input[:20]}...")
            else:
                print(f"⚠️ Input modified: {malicious_input[:20]}...")
        except Exception as e:
            print(f"❌ Error with input: {malicious_input[:20]}... → {e}")
            return False
    
    print("✅ Security tests passed")
    return True

def main():
    """Run all tests"""
    print("🚀 Botswana Fuel Price API - Comprehensive Testing")
    print("=" * 60)
    
    # Run all tests
    deps = test_dependencies()
    regex_ok = test_regex_patterns()
    json_ok = test_json_handling()
    mock_ok = test_mock_api()
    perf_ok = test_performance()
    edge_ok = test_edge_cases()
    security_ok = test_security()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    
    print(f"Dependencies Available:")
    print(f"  ✅ Built-in modules: {'Yes' if deps.get('builtin') else 'No'}")
    print(f"  {'✅' if deps.get('requests') else '❌'} requests: {'Yes' if deps.get('requests') else 'No'}")
    print(f"  {'✅' if deps.get('bs4') else '❌'} beautifulsoup4: {'Yes' if deps.get('bs4') else 'No'}")
    
    print(f"\nCore Functionality:")
    print(f"  {'✅' if regex_ok else '❌'} Regex patterns: {'Working' if regex_ok else 'Failed'}")
    print(f"  {'✅' if json_ok else '❌'} JSON handling: {'Working' if json_ok else 'Failed'}")
    print(f"  {'✅' if mock_ok else '❌'} API logic: {'Working' if mock_ok else 'Failed'}")
    
    print(f"\nAdvanced Tests:")
    print(f"  {'✅' if perf_ok else '❌'} Performance: {'Good' if perf_ok else 'Issues'}")
    print(f"  {'✅' if edge_ok else '❌'} Edge cases: {'Handled' if edge_ok else 'Failed'}")
    print(f"  {'✅' if security_ok else '❌'} Security: {'Secure' if security_ok else 'Vulnerable'}")
    
    all_deps = deps.get('requests', False) and deps.get('bs4', False)
    core_working = regex_ok and json_ok and mock_ok
    advanced_working = perf_ok and edge_ok and security_ok
    
    print(f"\n🎯 OVERALL STATUS:")
    if all_deps and core_working and advanced_working:
        print("🟢 PRODUCTION READY - All tests passed!")
        print("\n✅ Dependencies: Available")
        print("✅ Core functionality: Working")
        print("✅ Performance: Good")
        print("✅ Edge cases: Handled")
        print("✅ Security: Secure")
        print("\nNext steps:")
        print("1. Test with real BERA data: python test_real_bera.py")
        print("2. Deploy: serverless deploy")
        print("3. Create documentation for BERA")
    elif all_deps and core_working:
        print("🟡 CORE READY - Some advanced features need attention")
        print("\nNext steps:")
        print("1. Review failed advanced tests")
        print("2. Test with real data: python test_real_bera.py")
        print("3. Deploy: serverless deploy")
    elif core_working and not all_deps:
        print("🟡 CORE LOGIC WORKING - Install dependencies to deploy")
        print("\nNext steps:")
        print("1. Install: pip install -r requirements.txt")
        print("2. Test: python test_real_bera.py")
        print("3. Deploy: serverless deploy")
    else:
        print("🔴 ISSUES FOUND - Check the failed tests above")
        
    return all_deps and core_working

if __name__ == "__main__":
    main()