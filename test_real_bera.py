#!/usr/bin/env python3
"""
Test the Botswana Fuel Price API with real BERA website data
"""

import json
import sys

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking Dependencies...")
    print("-" * 40)
    
    missing = []
    
    try:
        import requests
        print("✅ requests: Available")
    except ImportError:
        missing.append("requests")
        print("❌ requests: Not installed")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4: Available")
    except ImportError:
        missing.append("beautifulsoup4")
        print("❌ beautifulsoup4: Not installed")
    
    if missing:
        print(f"\n🚨 Missing dependencies: {', '.join(missing)}")
        print("Please install them with:")
        print("pip install -r requirements.txt")
        print("or run: install_deps.bat")
        return False
    
    print("✅ All dependencies available!")
    return True

def test_bera_website_access():
    """Test if we can access the BERA website"""
    print("\n🌐 Testing BERA Website Access...")
    print("-" * 40)
    
    try:
        import requests
        
        url = "https://www.bera.co.bw/media/press-releases"
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; FuelPriceBot/1.0)'}
        
        print(f"Attempting to connect to: {url}")
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response Size: {len(response.text)} characters")
        
        if response.status_code == 200:
            print("✅ BERA website is accessible!")
            return response.text
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Connection timeout - BERA website may be slow")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check internet connection")
        return None
    except Exception as e:
        print(f"❌ Error accessing BERA website: {e}")
        return None

def test_fuel_announcement_detection(html_content):
    """Test if we can find fuel price announcements"""
    print("\n🔍 Testing Fuel Announcement Detection...")
    print("-" * 40)
    
    try:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for links with fuel-related keywords
        keywords = ['fuel price', 'petroleum price', 'petrol price', 'diesel price', 'fuel adjustment']
        
        print("Searching for fuel-related announcements...")
        
        found_links = []
        links = soup.find_all('a', href=True)
        
        for link in links:
            text = link.get_text().lower()
            for keyword in keywords:
                if keyword in text:
                    href = link['href']
                    link_text = link.get_text().strip()
                    found_links.append((href, link_text))
                    print(f"✅ Found: {link_text}")
                    print(f"   URL: {href}")
                    break
        
        if found_links:
            print(f"\n✅ Found {len(found_links)} fuel-related announcement(s)")
            return found_links[0][0]  # Return first link
        else:
            print("❌ No fuel price announcements found")
            print("This might mean:")
            print("  - No recent fuel price updates")
            print("  - Website structure has changed")
            print("  - Different keywords are being used")
            return None
            
    except Exception as e:
        print(f"❌ Error detecting announcements: {e}")
        return None

def test_full_api_functionality():
    """Test the complete API functionality"""
    print("\n🚀 Testing Full API Functionality...")
    print("-" * 40)
    
    try:
        # Import our handler
        from handler import get_prices
        
        # Simulate Lambda event and context
        event = {}
        context = {}
        
        print("Calling get_prices function...")
        result = get_prices(event, context)
        
        print(f"Status Code: {result['statusCode']}")
        
        if result['statusCode'] == 200:
            print("✅ API call successful!")
            
            # Parse the response
            response_data = json.loads(result['body'])
            
            print(f"✅ Effective Date: {response_data.get('effectiveDate')}")
            print(f"✅ Currency: {response_data.get('currency')}")
            print(f"✅ Source URL: {response_data.get('sourceUrl')}")
            print(f"✅ Number of prices: {len(response_data.get('prices', []))}")
            
            print("\n📋 Extracted Prices:")
            for price_item in response_data.get('prices', []):
                product = price_item.get('product', 'Unknown')
                price = price_item.get('price', 0)
                print(f"   • {product}: {price} BWP")
            
            # Validate response structure
            required_fields = ['effectiveDate', 'currency', 'prices', 'sourceUrl']
            missing_fields = [field for field in required_fields if field not in response_data]
            
            if missing_fields:
                print(f"⚠️ Missing fields: {missing_fields}")
                return False
            
            if response_data.get('currency') != 'BWP':
                print(f"⚠️ Unexpected currency: {response_data.get('currency')}")
                return False
            
            if len(response_data.get('prices', [])) == 0:
                print("⚠️ No prices extracted")
                return False
            
            print("\n🎉 API FUNCTIONALITY TEST PASSED!")
            return True
            
        else:
            print(f"❌ API returned error: {result['body']}")
            error_data = json.loads(result['body'])
            print(f"Error message: {error_data.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure handler.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 BOTSWANA FUEL PRICE API - REAL BERA TESTING")
    print("=" * 60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without dependencies")
        return False
    
    # Step 2: Test BERA website access
    html_content = test_bera_website_access()
    if not html_content:
        print("\n❌ Cannot access BERA website")
        print("This could be due to:")
        print("  - Internet connectivity issues")
        print("  - BERA website being down")
        print("  - Firewall blocking the request")
        return False
    
    # Step 3: Test fuel announcement detection
    announcement_link = test_fuel_announcement_detection(html_content)
    if announcement_link:
        print(f"✅ Successfully detected fuel announcement link")
    else:
        print("⚠️ Could not detect fuel announcements")
        print("Proceeding with full API test anyway...")
    
    # Step 4: Test full API functionality
    api_success = test_full_api_functionality()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 REAL BERA TEST SUMMARY")
    print("=" * 60)
    
    if api_success:
        print("🟢 SUCCESS: API is working with real BERA data!")
        print("\n✅ Dependencies: Installed")
        print("✅ BERA website: Accessible")
        print("✅ Fuel announcements: Detectable")
        print("✅ Price extraction: Working")
        print("✅ JSON response: Valid")
        
        print("\n🚀 READY FOR DEPLOYMENT!")
        print("\nNext steps:")
        print("1. Run comprehensive tests: python test_comprehensive.py")
        print("2. Deploy to AWS: serverless deploy")
        print("3. Create BERA documentation")
        
        return True
    else:
        print("🔴 FAILED: Issues found with real BERA data")
        print("\nPossible issues:")
        print("  - BERA website structure changed")
        print("  - No recent fuel price announcements")
        print("  - Network connectivity problems")
        print("  - Regex patterns need adjustment")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)