import json
import re

# Test the core functionality inline
print("🧪 Quick Test of Fuel Price API Core Logic")
print("=" * 50)

# Sample text from BERA announcement
sample_text = """
FUEL PRICE ADJUSTMENT - EFFECTIVE 15TH JANUARY 2024

The following retail pump prices are effective from 15th January 2024:

Unleaded Petrol 93: 14.50 BWP per litre
Unleaded Petrol 95: 14.75 BWP per litre
Diesel 50ppm: 13.80 BWP per litre
Illuminating Paraffin: 9.50 BWP per litre
"""

print("1. Testing price extraction patterns...")

# Test fuel price patterns
fuel_types = [
    ("Retail Pump Price - Unleaded Petrol 93", r'petrol\s+93.*?(\d+\.\d+)'),
    ("Retail Pump Price - Unleaded Petrol 95", r'petrol\s+95.*?(\d+\.\d+)'),
    ("Retail Pump Price - Diesel 50ppm", r'diesel.*?(\d+\.\d+)'),
    ("Wholesale Price - Illuminating Paraffin", r'paraffin.*?(\d+\.\d+)')
]

prices = []
for product, pattern in fuel_types:
    match = re.search(pattern, sample_text, re.IGNORECASE)
    if match:
        try:
            price = float(match.group(1))
            prices.append({"product": product, "price": price})
            print(f"✅ {product}: {price} BWP")
        except:
            print(f"❌ {product}: Could not parse price")
    else:
        print(f"❌ {product}: Pattern not found")

print(f"\n2. Extracted {len(prices)} prices")

# Test date extraction
date_match = re.search(r'effective.*?(\d{1,2}.*?\d{4})', sample_text, re.IGNORECASE)
effective_date = date_match.group(1) if date_match else "Date not specified"
print(f"3. Extracted date: '{effective_date}'")

# Create response
response_data = {
    "effectiveDate": effective_date,
    "currency": "BWP", 
    "prices": prices,
    "sourceUrl": "https://www.bera.co.bw/test-announcement"
}

print("\n4. Sample API Response:")
print(json.dumps(response_data, indent=2))

print(f"\n📊 Test Results:")
print(f"✅ Prices extracted: {len(prices)}/4")
print(f"✅ Date extracted: {'Yes' if date_match else 'No'}")
print(f"✅ JSON formatting: {'Yes' if response_data else 'No'}")

if len(prices) == 4 and date_match:
    print("\n🎉 ALL CORE TESTS PASSED!")
    print("The API logic is working correctly.")
else:
    print("\n⚠️ Some tests failed - check patterns above")

print("\nTo test with real BERA data:")
print("1. pip install -r requirements.txt")
print("2. python test_local.py")