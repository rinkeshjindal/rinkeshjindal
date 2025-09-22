"""
Realistic Sample Data Generator for Bank Balance Checker
This creates realistic Indian bank data for development and demonstration
"""
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List

class RealisticSampleDataGenerator:
    """Generates realistic sample data for Indian banks."""
    
    def __init__(self):
        """Initialize the sample data generator."""
        self.bank_names = ['ICICI', 'AXIS', 'YES', 'HDFC']
        self.account_types = ['Savings', 'Current', 'Salary', 'PPF', 'NRE', 'NRO']
        self.fd_tenures = [30, 90, 180, 365, 730, 1095, 1825]  # days
        self.interest_rates = [5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5]
        
    def generate_realistic_accounts(self, bank: str, count: int = 2) -> List[Dict]:
        """Generate realistic account data for a bank."""
        accounts = []
        
        # Bank-specific account patterns
        bank_patterns = {
            'ICICI': {
                'account_prefix': '1234',
                'balance_range': (50000, 500000),
                'common_types': ['Savings', 'Current', 'Salary']
            },
            'AXIS': {
                'account_prefix': '1111',
                'balance_range': (75000, 750000),
                'common_types': ['Savings', 'Current', 'Salary']
            },
            'YES': {
                'account_prefix': '7777',
                'balance_range': (30000, 300000),
                'common_types': ['Savings', 'Current']
            },
            'HDFC': {
                'account_prefix': '5555',
                'balance_range': (100000, 1000000),
                'common_types': ['Savings', 'Current', 'PPF', 'NRE']
            }
        }
        
        pattern = bank_patterns.get(bank, bank_patterns['ICICI'])
        
        for i in range(count):
            account_number = f"{pattern['account_prefix']}{random.randint(100000, 999999)}"
            account_type = random.choice(pattern['common_types'])
            balance = random.uniform(*pattern['balance_range'])
            
            # Add some realistic variation
            if account_type == 'PPF':
                balance = random.uniform(100000, 500000)
            elif account_type == 'NRE':
                balance = random.uniform(200000, 800000)
            elif account_type == 'Salary':
                balance = random.uniform(80000, 300000)
            
            account = {
                'account_number': account_number,
                'account_type': account_type,
                'balance': round(balance, 2),
                'currency': 'INR',
                'last_updated': datetime.now().isoformat(),
                'ifsc_code': f"{bank}0001234",  # Mock IFSC
                'branch': f"{bank} Bank Main Branch",
                'opening_date': (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d')
            }
            accounts.append(account)
        
        return accounts
    
    def generate_realistic_fixed_deposits(self, bank: str, count: int = 2) -> List[Dict]:
        """Generate realistic fixed deposit data for a bank."""
        fds = []
        
        # Bank-specific FD patterns
        bank_fd_patterns = {
            'ICICI': {
                'fd_prefix': 'FD',
                'amount_range': (50000, 500000),
                'interest_range': (6.0, 7.5)
            },
            'AXIS': {
                'fd_prefix': 'AXISFD',
                'amount_range': (75000, 750000),
                'interest_range': (6.2, 7.8)
            },
            'YES': {
                'fd_prefix': 'YESFD',
                'amount_range': (30000, 300000),
                'interest_range': (5.8, 7.2)
            },
            'HDFC': {
                'fd_prefix': 'HDFCFD',
                'amount_range': (100000, 1000000),
                'interest_range': (6.5, 8.0)
            }
        }
        
        pattern = bank_fd_patterns.get(bank, bank_fd_patterns['ICICI'])
        
        for i in range(count):
            fd_number = f"{pattern['fd_prefix']}{random.randint(100000, 999999)}"
            principal_amount = random.uniform(*pattern['amount_range'])
            interest_rate = random.uniform(*pattern['interest_range'])
            tenure_days = random.choice(self.fd_tenures)
            maturity_date = datetime.now() + timedelta(days=tenure_days)
            
            # Calculate maturity amount (simple interest)
            years = tenure_days / 365.25
            maturity_amount = principal_amount * (1 + (interest_rate / 100) * years)
            
            fd = {
                'fd_number': fd_number,
                'principal_amount': round(principal_amount, 2),
                'interest_rate': round(interest_rate, 2),
                'maturity_date': maturity_date.strftime('%Y-%m-%d'),
                'maturity_amount': round(maturity_amount, 2),
                'days_to_maturity': tenure_days,
                'tenure_days': tenure_days,
                'opening_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                'status': 'Active',
                'auto_renewal': random.choice([True, False])
            }
            fds.append(fd)
        
        return fds
    
    def generate_realistic_transactions(self, account_number: str, count: int = 10) -> List[Dict]:
        """Generate realistic transaction data for an account."""
        transactions = []
        
        transaction_types = [
            'Salary Credit', 'ATM Withdrawal', 'Online Transfer', 'UPI Payment',
            'Cheque Deposit', 'Interest Credit', 'Bill Payment', 'Shopping',
            'Fuel Payment', 'Grocery', 'Restaurant', 'Entertainment'
        ]
        
        for i in range(count):
            transaction_date = datetime.now() - timedelta(days=random.randint(1, 30))
            amount = random.uniform(100, 50000)
            transaction_type = random.choice(transaction_types)
            
            # Determine if it's credit or debit
            if 'Credit' in transaction_type or 'Deposit' in transaction_type:
                amount = abs(amount)
                txn_type = 'credit'
            else:
                amount = -abs(amount)
                txn_type = 'debit'
            
            transaction = {
                'transaction_id': f"TXN{random.randint(100000, 999999)}",
                'date': transaction_date.strftime('%Y-%m-%d'),
                'time': transaction_date.strftime('%H:%M:%S'),
                'description': transaction_type,
                'amount': round(amount, 2),
                'type': txn_type,
                'balance': round(random.uniform(50000, 200000), 2),
                'reference': f"REF{random.randint(100000, 999999)}",
                'mode': random.choice(['UPI', 'NEFT', 'RTGS', 'ATM', 'Online', 'Cheque'])
            }
            transactions.append(transaction)
        
        # Sort by date (newest first)
        transactions.sort(key=lambda x: x['date'], reverse=True)
        return transactions
    
    def generate_complete_bank_data(self) -> Dict[str, Dict]:
        """Generate complete realistic data for all banks."""
        complete_data = {}
        
        for bank in self.bank_names:
            bank_data = {
                'bank': bank,
                'accounts': self.generate_realistic_accounts(bank, random.randint(1, 3)),
                'fixed_deposits': self.generate_realistic_fixed_deposits(bank, random.randint(1, 3)),
                'last_updated': datetime.now().isoformat(),
                'bank_info': {
                    'name': f"{bank} Bank",
                    'ifsc_code': f"{bank}0001234",
                    'branch': f"{bank} Bank Main Branch",
                    'address': f"{bank} Bank Building, Mumbai, Maharashtra 400001",
                    'phone': f"+91-22-{random.randint(10000000, 99999999)}",
                    'email': f"support@{bank.lower()}bank.com"
                }
            }
            
            # Add transactions for each account
            for account in bank_data['accounts']:
                account['transactions'] = self.generate_realistic_transactions(
                    account['account_number'], random.randint(5, 15)
                )
            
            complete_data[bank] = bank_data
        
        return complete_data
    
    def save_to_json(self, data: Dict, filename: str = "realistic_bank_data.json"):
        """Save the generated data to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Realistic sample data saved to {filename}")
    
    def print_summary(self, data: Dict):
        """Print a summary of the generated data."""
        print("\n" + "="*60)
        print("📊 REALISTIC SAMPLE DATA SUMMARY")
        print("="*60)
        
        total_balance = 0
        total_fd_amount = 0
        total_accounts = 0
        total_fds = 0
        
        for bank, bank_data in data.items():
            bank_balance = sum(acc['balance'] for acc in bank_data['accounts'])
            bank_fd_amount = sum(fd['principal_amount'] for fd in bank_data['fixed_deposits'])
            
            print(f"\n🏦 {bank} Bank:")
            print(f"   Accounts: {len(bank_data['accounts'])}")
            print(f"   Balance: ₹{bank_balance:,.2f}")
            print(f"   FDs: {len(bank_data['fixed_deposits'])}")
            print(f"   FD Amount: ₹{bank_fd_amount:,.2f}")
            
            total_balance += bank_balance
            total_fd_amount += bank_fd_amount
            total_accounts += len(bank_data['accounts'])
            total_fds += len(bank_data['fixed_deposits'])
        
        print(f"\n📈 TOTALS:")
        print(f"   Total Accounts: {total_accounts}")
        print(f"   Total Balance: ₹{total_balance:,.2f}")
        print(f"   Total FDs: {total_fds}")
        print(f"   Total FD Amount: ₹{total_fd_amount:,.2f}")
        print(f"   Total Portfolio: ₹{total_balance + total_fd_amount:,.2f}")
        print("="*60)

def main():
    """Generate and display realistic sample data."""
    print("🏦 Generating Realistic Sample Data for Indian Banks")
    print("="*60)
    
    generator = RealisticSampleDataGenerator()
    data = generator.generate_complete_bank_data()
    
    # Print summary
    generator.print_summary(data)
    
    # Save to file
    generator.save_to_json(data)
    
    print(f"\n💡 Use this data to build your prototype!")
    print(f"📁 Data saved to: realistic_bank_data.json")
    print(f"🔧 Import this data into your application")

if __name__ == "__main__":
    main()