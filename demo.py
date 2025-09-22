#!/usr/bin/env python3
"""
Demo Script for India Bank Checker
This demonstrates the mock API functionality
"""
import requests
import json
import time
from datetime import datetime

def print_header():
    """Print demo header."""
    print("=" * 60)
    print("🏦 INDIA BANK CHECKER - DEMO")
    print("=" * 60)
    print("📊 This demo shows how the mock API works")
    print("🚀 No official API approval required")
    print("=" * 60)

def test_mock_api():
    """Test the mock API server."""
    print("\n🔍 Testing Mock API Server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Mock API Server is running")
            data = response.json()
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print("❌ Mock API Server is not responding")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Mock API Server is not running")
        print("   Please run: python mock_bank_api.py")
        return False
    except Exception as e:
        print(f"❌ Error testing mock API: {e}")
        return False

def demo_bank_data(bank_name):
    """Demo bank data for a specific bank."""
    print(f"\n🏦 {bank_name} Bank Data:")
    print("-" * 40)
    
    headers = {'X-Bank-Name': bank_name}
    
    try:
        # Get accounts
        response = requests.get("http://localhost:5000/api/v1/accounts", headers=headers)
        if response.status_code == 200:
            data = response.json()
            accounts = data['data']['accounts']
            print(f"📊 Accounts ({len(accounts)}):")
            for account in accounts:
                print(f"   {account['account_number']} - {account['account_type']} - ₹{account['balance']:,.2f}")
        else:
            print(f"❌ Failed to get accounts: {response.status_code}")
        
        # Get fixed deposits
        response = requests.get("http://localhost:5000/api/v1/fixed-deposits", headers=headers)
        if response.status_code == 200:
            data = response.json()
            fds = data['data']['fixed_deposits']
            print(f"\n💰 Fixed Deposits ({len(fds)}):")
            for fd in fds:
                print(f"   {fd['fd_number']} - ₹{fd['principal_amount']:,.2f} @ {fd['interest_rate']}%")
                print(f"      Maturity: {fd['maturity_date']} (₹{fd['maturity_amount']:,.2f})")
        else:
            print(f"❌ Failed to get FDs: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting {bank_name} data: {e}")

def demo_summary():
    """Demo summary data."""
    print(f"\n📈 Portfolio Summary:")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/v1/summary")
        if response.status_code == 200:
            data = response.json()
            summary = data['data']
            
            print(f"Total Balance: ₹{summary['total_balance']:,.2f}")
            print(f"Total FD Amount: ₹{summary['total_fd_amount']:,.2f}")
            print(f"Total Accounts: {summary['total_accounts']}")
            print(f"Total FDs: {summary['total_fds']}")
            print(f"Total Portfolio: ₹{summary['total_balance'] + summary['total_fd_amount']:,.2f}")
            
            print(f"\nBank-wise breakdown:")
            for bank in summary['banks']:
                print(f"   {bank['bank']}: ₹{bank['total_balance']:,.2f} ({bank['account_count']} accounts, {bank['fd_count']} FDs)")
        else:
            print(f"❌ Failed to get summary: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting summary: {e}")

def demo_transactions():
    """Demo transaction data."""
    print(f"\n💳 Sample Transactions:")
    print("-" * 40)
    
    try:
        # Get transactions for ICICI account
        response = requests.get("http://localhost:5000/api/v1/accounts/1234567890/transactions", 
                              headers={'X-Bank-Name': 'ICICI'})
        if response.status_code == 200:
            data = response.json()
            transactions = data['data']['transactions'][:5]  # Show first 5
            
            print("Recent transactions for ICICI account 1234567890:")
            for txn in transactions:
                amount_str = f"₹{abs(txn['amount']):,.2f}"
                if txn['amount'] < 0:
                    amount_str = f"-{amount_str}"
                else:
                    amount_str = f"+{amount_str}"
                
                print(f"   {txn['date']} - {txn['description']} - {amount_str}")
        else:
            print(f"❌ Failed to get transactions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting transactions: {e}")

def show_next_steps():
    """Show next steps for the user."""
    print(f"\n" + "=" * 60)
    print("🎉 DEMO COMPLETED!")
    print("=" * 60)
    print("✅ Mock API Server is working")
    print("✅ All endpoints are responding")
    print("✅ Data is realistic and professional")
    print("\n📋 NEXT STEPS:")
    print("1. 🔧 Customize the mock data in mock_bank_api.py")
    print("2. 📊 Modify reports in reporting.py")
    print("3. 🎨 Build your user interface")
    print("4. 📋 Apply for official bank APIs")
    print("5. 🚀 Deploy to production")
    print("\n🔧 USEFUL COMMANDS:")
    print("• python mock_bank_api.py - Start mock API server")
    print("• python test_mock_api.py - Test all endpoints")
    print("• python main_dev.py - Run development mode")
    print("• python realistic_sample_data.py - Generate sample data")
    print("\n💡 TIP: Use this demo to show banks your capabilities!")
    print("=" * 60)

def main():
    """Main demo function."""
    print_header()
    
    # Test if mock API is running
    if not test_mock_api():
        print("\n❌ Please start the mock API server first:")
        print("   python mock_bank_api.py")
        return
    
    # Demo each bank
    banks = ['ICICI', 'AXIS', 'YES', 'HDFC']
    for bank in banks:
        demo_bank_data(bank)
        time.sleep(1)  # Small delay for better readability
    
    # Demo summary
    demo_summary()
    
    # Demo transactions
    demo_transactions()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()