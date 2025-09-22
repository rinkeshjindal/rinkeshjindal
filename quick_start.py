#!/usr/bin/env python3
"""
Quick Start Script for India Bank Checker
This script helps you get started immediately with mock APIs
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("🏦 INDIA BANK CHECKER - QUICK START")
    print("=" * 60)
    print("🚀 Get started immediately with mock APIs")
    print("📊 No official API approval required")
    print("🔧 Perfect for development and testing")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'requests', 'pandas', 'openpyxl', 
        'google-auth', 'cryptography', 'keyring'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def create_directories():
    """Create required directories."""
    print("\n📁 Creating required directories...")
    
    directories = ['logs', 'output', 'credentials']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def start_mock_api():
    """Start the mock API server."""
    print("\n🚀 Starting Mock API Server...")
    print("📊 This simulates real bank APIs for development")
    print("🌐 Server will be available at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Start the mock API server
        process = subprocess.Popen([sys.executable, "mock_bank_api.py"])
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server is running
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Mock API Server started successfully!")
                return process
            else:
                print("❌ Mock API Server failed to start")
                return None
        except:
            print("❌ Mock API Server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting mock API server: {e}")
        return None

def test_mock_apis():
    """Test the mock APIs."""
    print("\n🧪 Testing Mock APIs...")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, "test_mock_api.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Mock APIs working correctly!")
            print("📊 Test results:")
            print(result.stdout)
        else:
            print("❌ Mock API tests failed")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out - this might indicate an issue")
        return False
    except Exception as e:
        print(f"❌ Error testing mock APIs: {e}")
        return False
    
    return True

def run_development_mode():
    """Run the development mode application."""
    print("\n🚀 Running Development Mode...")
    print("📊 This will generate sample reports using mock data")
    print("=" * 60)
    
    try:
        # Run the development mode
        result = subprocess.run([sys.executable, "main_dev.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Development mode completed successfully!")
            print("📊 Output:")
            print(result.stdout)
            return True
        else:
            print("❌ Development mode failed")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Development mode timed out")
        return False
    except Exception as e:
        print(f"❌ Error running development mode: {e}")
        return False

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 QUICK START COMPLETED!")
    print("=" * 60)
    print("✅ Mock API Server is running")
    print("✅ All tests passed")
    print("✅ Development mode working")
    print("\n📋 NEXT STEPS:")
    print("1. 🔧 Customize the mock data in mock_bank_api.py")
    print("2. 📊 Modify reports in reporting.py")
    print("3. 🎨 Build your user interface")
    print("4. 📋 Apply for official bank APIs")
    print("5. 🚀 Deploy to production")
    print("\n📁 FILES CREATED:")
    print("• logs/ - Application logs")
    print("• output/ - Generated reports")
    print("• credentials/ - Secure credential storage")
    print("\n🔧 USEFUL COMMANDS:")
    print("• python mock_bank_api.py - Start mock API server")
    print("• python test_mock_api.py - Test mock APIs")
    print("• python main_dev.py - Run development mode")
    print("• python main.py - Run production mode (with real APIs)")
    print("\n📚 DOCUMENTATION:")
    print("• README.md - Complete setup guide")
    print("• API_DOCUMENTATION.md - Bank API details")
    print("• BREAKING_THE_CATCH22.md - Development strategies")
    print("\n💡 TIP: Use this prototype to demonstrate your application")
    print("   to banks when applying for official API access!")
    print("=" * 60)

def main():
    """Main quick start function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Failed to create directories")
        sys.exit(1)
    
    # Start mock API server
    process = start_mock_api()
    if not process:
        print("\n❌ Failed to start mock API server")
        sys.exit(1)
    
    try:
        # Test mock APIs
        if not test_mock_apis():
            print("\n❌ Mock API tests failed")
            return
        
        # Run development mode
        if not run_development_mode():
            print("\n❌ Development mode failed")
            return
        
        # Show next steps
        show_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Quick start interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        # Stop the mock API server
        if process:
            print("\n⏹️  Stopping Mock API Server...")
            process.terminate()
            print("✅ Mock API Server stopped")

if __name__ == "__main__":
    main()