#!/usr/bin/env python3
"""
Check current directory and list files
"""

import os
import sys

def check_directory():
    """Check current directory and list files"""
    print("📁 Directory Check for Botswana Fuel Price API")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # List all files
    print(f"\nFiles in current directory:")
    files = os.listdir('.')
    
    # Categorize files
    api_files = []
    test_files = []
    config_files = []
    other_files = []
    
    for file in files:
        if file.endswith('.py') and 'test' in file:
            test_files.append(file)
        elif file in ['handler.py', 'serverless.yml', 'requirements.txt']:
            api_files.append(file)
        elif file.endswith(('.md', '.txt', '.yml', '.yaml')):
            config_files.append(file)
        else:
            other_files.append(file)
    
    # Display categorized files
    if api_files:
        print(f"\n🔧 Core API Files:")
        for file in sorted(api_files):
            print(f"  ✅ {file}")
    
    if test_files:
        print(f"\n🧪 Test Files:")
        for file in sorted(test_files):
            print(f"  ✅ {file}")
    
    if config_files:
        print(f"\n📋 Documentation/Config Files:")
        for file in sorted(config_files):
            print(f"  📄 {file}")
    
    if other_files:
        print(f"\n📁 Other Files:")
        for file in sorted(other_files):
            print(f"  📄 {file}")
    
    # Check if we have the essential files
    essential_files = ['handler.py', 'serverless.yml', 'requirements.txt']
    missing_files = [f for f in essential_files if f not in files]
    
    print(f"\n📊 Status Check:")
    if not missing_files:
        print("✅ All essential API files present")
        
        # Check for test files
        test_files_needed = ['test_core.py', 'test_real_bera.py']
        missing_tests = [f for f in test_files_needed if f not in files]
        
        if not missing_tests:
            print("✅ Test files present")
            print("\n🚀 Ready to run tests!")
            print("\nNext steps:")
            print("1. Fix PowerShell: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser")
            print("2. Install deps: pip install -r requirements.txt")
            print("3. Run tests: python test_core.py")
        else:
            print(f"⚠️ Missing test files: {missing_tests}")
    else:
        print(f"❌ Missing essential files: {missing_files}")
        print("Make sure you're in the beraAPI directory")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = check_directory()
    if not success:
        print(f"\n💡 Tip: If you're not in the beraAPI directory, navigate there first:")
        print(f"   cd beraAPI")
    sys.exit(0 if success else 1)