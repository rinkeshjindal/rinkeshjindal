"""
Mock Bank Integration for Development and Testing
This allows you to build and test your application without official API approval
"""
import requests
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from bank_integration import BankAccount, FixedDeposit, BankAPI

logger = logging.getLogger(__name__)

class MockBankAPI(BankAPI):
    """Mock implementation of bank API for development."""
    
    def __init__(self, bank_name: str, username: str, password: str, api_key: str = None):
        super().__init__(bank_name, username, password, api_key)
        self.mock_api_url = "http://localhost:5000"  # Mock API server URL
    
    def authenticate(self) -> bool:
        """Mock authentication - always returns True for development."""
        try:
            logger.info(f"Mock authentication for {self.bank_name} - using mock API")
            
            # Test connection to mock API
            response = requests.get(f"{self.mock_api_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"Mock API connection successful for {self.bank_name}")
                return True
            else:
                logger.error(f"Mock API connection failed for {self.bank_name}")
                return False
                
        except Exception as e:
            logger.error(f"Mock authentication failed for {self.bank_name}: {e}")
            return False
    
    def get_accounts(self) -> List[BankAccount]:
        """Get accounts from mock API."""
        try:
            logger.info(f"Fetching accounts from mock API for {self.bank_name}")
            
            headers = {'X-Bank-Name': self.bank_name}
            response = requests.get(
                f"{self.mock_api_url}/api/v1/accounts",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                accounts = []
                
                for account_data in data['data']['accounts']:
                    account = BankAccount(
                        account_number=account_data['account_number'],
                        account_type=account_data['account_type'],
                        balance=float(account_data['balance']),
                        last_updated=datetime.fromisoformat(account_data['last_updated'])
                    )
                    accounts.append(account)
                
                logger.info(f"Retrieved {len(accounts)} accounts for {self.bank_name}")
                return accounts
            else:
                logger.error(f"Failed to get accounts for {self.bank_name}: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching accounts for {self.bank_name}: {e}")
            return []
    
    def get_fixed_deposits(self) -> List[FixedDeposit]:
        """Get fixed deposits from mock API."""
        try:
            logger.info(f"Fetching fixed deposits from mock API for {self.bank_name}")
            
            headers = {'X-Bank-Name': self.bank_name}
            response = requests.get(
                f"{self.mock_api_url}/api/v1/fixed-deposits",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                fixed_deposits = []
                
                for fd_data in data['data']['fixed_deposits']:
                    fd = FixedDeposit(
                        fd_number=fd_data['fd_number'],
                        principal_amount=float(fd_data['principal_amount']),
                        interest_rate=float(fd_data['interest_rate']),
                        maturity_date=datetime.strptime(fd_data['maturity_date'], '%Y-%m-%d'),
                        maturity_amount=float(fd_data['maturity_amount'])
                    )
                    fixed_deposits.append(fd)
                
                logger.info(f"Retrieved {len(fixed_deposits)} fixed deposits for {self.bank_name}")
                return fixed_deposits
            else:
                logger.error(f"Failed to get fixed deposits for {self.bank_name}: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching fixed deposits for {self.bank_name}: {e}")
            return []

class MockBankAPIFactory:
    """Factory class for creating mock bank API instances."""
    
    @staticmethod
    def create_mock_bank_api(bank_name: str, username: str, password: str, api_key: str = None) -> MockBankAPI:
        """Create a mock bank API instance."""
        return MockBankAPI(bank_name, username, password, api_key)

def start_mock_api_server():
    """Start the mock API server for development."""
    import subprocess
    import sys
    import time
    
    try:
        print("🚀 Starting Mock Bank API Server...")
        print("📊 This allows you to develop and test without official API approval")
        print("🌐 Server will be available at: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the mock API server
        process = subprocess.Popen([sys.executable, "mock_bank_api.py"])
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server is running
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Mock API Server started successfully!")
                print("🧪 You can now run: python test_mock_api.py")
                print("🔧 Or use the mock APIs in your application")
            else:
                print("❌ Mock API Server failed to start")
        except:
            print("❌ Mock API Server failed to start")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping Mock API Server...")
            process.terminate()
            print("✅ Mock API Server stopped")
            
    except Exception as e:
        print(f"❌ Error starting mock API server: {e}")

if __name__ == "__main__":
    start_mock_api_server()