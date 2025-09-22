"""
Test script for Mock Bank API
This demonstrates how to use the mock API for development
"""
import requests
import json
from datetime import datetime

# Mock API base URL
BASE_URL = "http://localhost:5000"

def test_bank_api(bank_name):
    """Test API for a specific bank"""
    print(f"\n🏦 Testing {bank_name} Bank API")
    print("=" * 50)
    
    headers = {'X-Bank-Name': bank_name}
    
    try:
        # Test accounts endpoint
        print(f"📊 Getting accounts for {bank_name}...")
        response = requests.get(f"{BASE_URL}/api/v1/accounts", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['data']['accounts'])} accounts")
            for account in data['data']['accounts']:
                print(f"   Account: {account['account_number']} - ₹{account['balance']:,.2f}")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # Test fixed deposits endpoint
        print(f"\n💰 Getting fixed deposits for {bank_name}...")
        response = requests.get(f"{BASE_URL}/api/v1/fixed-deposits", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['data']['fixed_deposits'])} fixed deposits")
            for fd in data['data']['fixed_deposits']:
                print(f"   FD: {fd['fd_number']} - ₹{fd['principal_amount']:,.2f} @ {fd['interest_rate']}%")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # Test specific account balance
        if bank_name in ['ICICI', 'AXIS', 'YES', 'HDFC']:
            account_id = "1234567890" if bank_name == 'ICICI' else "1111222233"
            print(f"\n🔍 Getting balance for account {account_id}...")
            response = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}/balance", headers=headers)
            if response.status_code == 200:
                data = response.json()
                account = data['data']['account']
                print(f"✅ Balance: ₹{account['balance']:,.2f}")
            else:
                print(f"❌ Error: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to mock API server")
        print("   Make sure to run: python mock_bank_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_summary():
    """Test summary endpoint"""
    print(f"\n📈 Getting summary for all banks")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/summary")
        if response.status_code == 200:
            data = response.json()
            summary = data['data']
            print(f"✅ Total Balance: ₹{summary['total_balance']:,.2f}")
            print(f"✅ Total FD Amount: ₹{summary['total_fd_amount']:,.2f}")
            print(f"✅ Total Accounts: {summary['total_accounts']}")
            print(f"✅ Total FDs: {summary['total_fds']}")
            print(f"\n📊 Bank-wise breakdown:")
            for bank in summary['banks']:
                print(f"   {bank['bank']}: ₹{bank['total_balance']:,.2f} ({bank['account_count']} accounts, {bank['fd_count']} FDs)")
        else:
            print(f"❌ Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to mock API server")
        print("   Make sure to run: python mock_bank_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    """Test health endpoint"""
    print(f"\n🏥 Testing API health")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"✅ Version: {data['version']}")
            print(f"✅ Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to mock API server")
        print("   Make sure to run: python mock_bank_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Mock Bank API Test Suite")
    print("=" * 50)
    
    # Test health first
    test_health()
    
    # Test each bank
    banks = ['ICICI', 'AXIS', 'YES', 'HDFC']
    for bank in banks:
        test_bank_api(bank)
    
    # Test summary
    test_summary()
    
    print(f"\n✅ Test completed!")
    print(f"💡 Use this mock API to build your prototype while waiting for official approval")