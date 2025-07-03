#!/usr/bin/env python3
"""
Test runner for Botswana Fuel Price API
Guides through the testing process step by step
"""

import sys
import subprocess
import os

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, title):
    """Print a formatted step"""
    print(f"\n{step_num}️⃣ {title}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is compatible"""
    print_step(0, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.7+ required")
        return False

def check_files():
    """Check if all required files exist"""
    print_step(1, "Checking Project Files")
    
    required_files = [
        'handler.py',
        'serverless.yml', 
        'requirements.txt',
        'test_core.py',
        'test_comprehensive.py',
        'test_real_bera.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n🚨 Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def run_core_tests():
    """Run core functionality tests"""
    print_step(2, "Running Core Functionality Tests")
    
    try:
        result = subprocess.run([sys.executable, 'test_core.py'], 
                              capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Core tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running core tests: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print_step(3, "Installing Dependencies")
    
    try:
        print("Installing requests...")
        result1 = subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests==2.31.0'], 
                                capture_output=True, text=True)
        
        print("Installing beautifulsoup4...")
        result2 = subprocess.run([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4==4.12.2'], 
                                capture_output=True, text=True)
        
        if result1.returncode == 0 and result2.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            if result1.stderr:
                print("requests error:", result1.stderr)
            if result2.stderr:
                print("beautifulsoup4 error:", result2.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_real_bera_tests():
    """Run tests with real BERA data"""
    print_step(4, "Testing with Real BERA Data")
    
    try:
        result = subprocess.run([sys.executable, 'test_real_bera.py'], 
                              capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ BERA tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running BERA tests: {e}")
        return False

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print_step(5, "Running Comprehensive Test Suite")
    
    try:
        result = subprocess.run([sys.executable, 'test_comprehensive.py'], 
                              capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Comprehensive tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running comprehensive tests: {e}")
        return False

def main():
    """Main test runner"""
    print_header("BOTSWANA FUEL PRICE API - COMPLETE TEST SUITE")
    
    # Track test results
    results = {}
    
    # Step 0: Check Python version
    results['python'] = check_python_version()
    if not results['python']:
        print("\n❌ Cannot proceed with incompatible Python version")
        return False
    
    # Step 1: Check files
    results['files'] = check_files()
    if not results['files']:
        print("\n❌ Cannot proceed with missing files")
        return False
    
    # Step 2: Run core tests
    results['core'] = run_core_tests()
    
    # Step 3: Install dependencies
    results['deps'] = install_dependencies()
    
    # Step 4: Run real BERA tests (only if deps installed)
    if results['deps']:
        results['bera'] = run_real_bera_tests()
    else:
        results['bera'] = False
        print("⏭️ Skipping BERA tests due to dependency issues")
    
    # Step 5: Run comprehensive tests (only if BERA tests passed)
    if results['bera']:
        results['comprehensive'] = run_comprehensive_tests()
    else:
        results['comprehensive'] = False
        print("⏭️ Skipping comprehensive tests due to BERA test issues")
    
    # Final summary
    print_header("FINAL TEST RESULTS")
    
    print("Test Results:")
    print(f"  {'✅' if results['python'] else '❌'} Python version: {'Compatible' if results['python'] else 'Incompatible'}")
    print(f"  {'✅' if results['files'] else '❌'} Project files: {'Present' if results['files'] else 'Missing'}")
    print(f"  {'✅' if results['core'] else '❌'} Core functionality: {'Working' if results['core'] else 'Failed'}")
    print(f"  {'✅' if results['deps'] else '❌'} Dependencies: {'Installed' if results['deps'] else 'Failed'}")
    print(f"  {'✅' if results['bera'] else '❌'} BERA integration: {'Working' if results['bera'] else 'Failed'}")
    print(f"  {'✅' if results['comprehensive'] else '❌'} Comprehensive tests: {'Passed' if results['comprehensive'] else 'Failed'}")
    
    # Overall status
    all_passed = all(results.values())
    critical_passed = results['python'] and results['files'] and results['core'] and results['deps']
    
    print(f"\n🎯 OVERALL STATUS:")
    if all_passed:
        print("🟢 ALL TESTS PASSED - PRODUCTION READY!")
        print("\n🚀 Your API is ready for:")
        print("  ✅ Deployment to AWS")
        print("  ✅ Integration with BERA data")
        print("  ✅ Production use")
        
        print("\n📋 Next Steps:")
        print("1. Deploy to AWS: serverless deploy")
        print("2. Create BERA documentation")
        print("3. Set up monitoring")
        
    elif critical_passed and results['bera']:
        print("🟡 CORE FUNCTIONALITY READY")
        print("\n✅ API works with real BERA data")
        print("⚠️ Some advanced tests failed")
        
        print("\n📋 Next Steps:")
        print("1. Review comprehensive test failures")
        print("2. Deploy to AWS: serverless deploy")
        print("3. Create BERA documentation")
        
    elif critical_passed:
        print("🟡 BASIC FUNCTIONALITY READY")
        print("\n✅ Core logic works")
        print("❌ BERA integration issues")
        
        print("\n📋 Next Steps:")
        print("1. Check internet connection")
        print("2. Verify BERA website accessibility")
        print("3. Review BERA test failures")
        
    else:
        print("🔴 CRITICAL ISSUES FOUND")
        print("\n❌ Basic functionality problems")
        
        print("\n📋 Next Steps:")
        print("1. Fix critical issues above")
        print("2. Re-run tests")
        print("3. Check project setup")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 CONGRATULATIONS! Your API is ready for deployment!")
    else:
        print("🔧 Please address the issues above and re-run the tests.")
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1)