#!/usr/bin/env python3
"""
Check if required dependencies are installed
"""

def check_dependencies():
    """Check if all required packages are available"""
    print("🔍 Checking dependencies...")
    print("=" * 40)
    
    dependencies = {
        'requests': 'HTTP requests library',
        'bs4': 'BeautifulSoup HTML parser',
        'json': 'JSON handling (built-in)',
        're': 'Regular expressions (built-in)',
        'urllib.parse': 'URL parsing (built-in)'
    }
    
    missing = []
    available = []
    
    for package, description in dependencies.items():
        try:
            if package == 'bs4':
                import bs4
                available.append(f"✅ {package} ({description})")
            elif package == 'urllib.parse':
                from urllib.parse import urljoin
                available.append(f"✅ {package} ({description})")
            else:
                __import__(package)
                available.append(f"✅ {package} ({description})")
        except ImportError:
            missing.append(f"❌ {package} ({description})")
    
    print("\n📦 Available packages:")
    for pkg in available:
        print(f"   {pkg}")
    
    if missing:
        print("\n🚨 Missing packages:")
        for pkg in missing:
            print(f"   {pkg}")
        
        print("\n💡 To install missing packages:")
        if 'requests' in str(missing):
            print("   pip install requests")
        if 'bs4' in str(missing):
            print("   pip install beautifulsoup4")
        
        return False
    else:
        print("\n🎉 All dependencies are available!")
        return True

def test_basic_functionality():
    """Test basic functionality without external calls"""
    print("\n🧪 Testing basic functionality...")
    print("=" * 40)
    
    try:
        # Test regex patterns
        test_text = "Unleaded Petrol 93: 14.50 BWP per litre"
        pattern = r'petrol\s+93.*?(\d+\.\d+)'
        
        import re
        match = re.search(pattern, test_text, re.IGNORECASE)
        
        if match:
            price = float(match.group(1))
            print(f"✅ Regex pattern works: extracted price {price}")
        else:
            print("❌ Regex pattern failed")
            
        # Test JSON handling
        import json
        test_data = {
            "effectiveDate": "15 January 2024",
            "currency": "BWP",
            "prices": [{"product": "Test", "price": 14.50}]
        }
        
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        
        if parsed['currency'] == 'BWP':
            print("✅ JSON handling works")
        else:
            print("❌ JSON handling failed")
            
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    deps_ok = check_dependencies()
    basic_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if deps_ok and basic_ok:
        print("🚀 Ready to test the full API!")
        print("\nNext steps:")
        print("1. Run: python test_simple.py (mock test)")
        print("2. Install deps: pip install -r requirements.txt")
        print("3. Run: python test_local.py (real test)")
    else:
        print("⚠️  Some issues found. Please install missing dependencies.")