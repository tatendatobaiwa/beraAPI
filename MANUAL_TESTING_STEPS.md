# Manual Testing Steps for Botswana Fuel Price API

## 🚨 **Current Issue**
PowerShell execution policy is blocking all script execution. We need to fix this first.

---

## 🔧 **Step 1: Fix PowerShell Execution Policy**

### **Option A: Using Command Prompt (Recommended)**

1. **Open Command Prompt as Administrator**
   - Press `Win + R`
   - Type `cmd`
   - Press `Ctrl + Shift + Enter` (to run as admin)

2. **Run this command:**
   ```cmd
   powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
   ```

### **Option B: Using PowerShell Directly**

1. **Open PowerShell as Administrator**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)"

2. **Run this command:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   ```

3. **Verify the fix:**
   ```powershell
   Get-ExecutionPolicy
   ```
   Should show: `RemoteSigned`

---

## 📁 **Step 2: Navigate to beraAPI Directory**

1. **Open Command Prompt or PowerShell**
2. **Navigate to your project:**
   ```cmd
   cd C:\Users\taten\APIs\beraAPI
   ```
   (Adjust path as needed)

3. **Verify you're in the right place:**
   ```cmd
   dir
   ```
   You should see files like:
   - `handler.py`
   - `serverless.yml`
   - `requirements.txt`
   - `test_core.py`
   - etc.

---

## 🧪 **Step 3: Run the Tests**

### **Install Dependencies First:**
```cmd
pip install requests==2.31.0 beautifulsoup4==4.12.2
```

### **Test 1: Core Functionality (No Internet Required)**
```cmd
python test_core.py
```

**Expected Output:**
```
🧪 Quick Test of Fuel Price API Core Logic
==================================================
1. Testing price extraction patterns...
✅ Retail Pump Price - Unleaded Petrol 93: 14.5 BWP
✅ Retail Pump Price - Unleaded Petrol 95: 14.75 BWP
✅ Retail Pump Price - Diesel 50ppm: 13.8 BWP
✅ Wholesale Price - Illuminating Paraffin: 9.5 BWP

🎉 ALL CORE TESTS PASSED!
```

### **Test 2: Real BERA Website Integration**
```cmd
python test_real_bera.py
```

**Expected Output:**
```
🧪 BOTSWANA FUEL PRICE API - REAL BERA TESTING
============================================================
✅ Dependencies: Available
✅ BERA website: Accessible
✅ Fuel announcements: Detectable
✅ Price extraction: Working
✅ JSON response: Valid

🟢 SUCCESS: API is working with real BERA data!
```

### **Test 3: Comprehensive Test Suite**
```cmd
python test_comprehensive.py
```

**Expected Output:**
```
🟢 PRODUCTION READY - All tests passed!
✅ Dependencies: Available
✅ Core functionality: Working
✅ Performance: Good
✅ Edge cases: Handled
✅ Security: Secure
```

---

## 🎯 **Step 4: Test the Actual API Function**

### **Test the Lambda Handler:**
```cmd
python test_local.py
```

This will call the actual `get_prices()` function and show you real fuel prices from BERA!

---

## 📊 **What Each Test Does**

| Test File | Purpose | Internet Required |
|-----------|---------|-------------------|
| `test_core.py` | Tests regex patterns and JSON formatting | ❌ No |
| `test_real_bera.py` | Tests connection to BERA website | ✅ Yes |
| `test_comprehensive.py` | Performance, security, edge cases | ❌ No |
| `test_local.py` | Tests actual API function | ✅ Yes |

---

## 🚨 **Troubleshooting**

### **If PowerShell Still Blocked:**
```cmd
powershell -ExecutionPolicy Bypass -Command "Get-ExecutionPolicy"
```

### **If Python Not Found:**
```cmd
python --version
```
If this fails, Python isn't in your PATH.

### **If Dependencies Fail to Install:**
```cmd
pip --version
pip list
```

### **If BERA Website Test Fails:**
- Check internet connection
- Try: `ping bera.co.bw`
- BERA website might be down temporarily

---

## 🎉 **Success Criteria**

✅ **All tests pass** = Ready for deployment!  
✅ **Core tests pass** = API logic works  
✅ **BERA tests pass** = Real integration works  

---

## 📋 **Next Steps After Tests Pass**

1. **Deploy to AWS:**
   ```cmd
   serverless deploy
   ```

2. **Create BERA presentation** using `BERA_DOCUMENTATION.md`

3. **Set up monitoring** and alerts

---

**Ready to start? Run these commands in order:**

1. `powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"`
2. `cd C:\Users\taten\APIs\beraAPI`
3. `pip install requests==2.31.0 beautifulsoup4==4.12.2`
4. `python test_core.py`
5. `python test_real_bera.py`

Let me know what output you get! 🚀