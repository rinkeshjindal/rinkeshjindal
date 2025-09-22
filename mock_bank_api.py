"""
Mock Bank API Server for Development and Testing
This simulates real bank API responses without requiring official approval
"""
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)

# Mock data for different banks
MOCK_DATA = {
    'ICICI': {
        'accounts': [
            {
                'account_number': '1234567890',
                'account_type': 'Savings',
                'balance': 125000.50,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            },
            {
                'account_number': '0987654321',
                'account_type': 'Current',
                'balance': 75000.00,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            }
        ],
        'fixed_deposits': [
            {
                'fd_number': 'FD123456',
                'principal_amount': 100000.00,
                'interest_rate': 6.5,
                'maturity_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                'maturity_amount': 106500.00,
                'days_to_maturity': 365
            },
            {
                'fd_number': 'FD789012',
                'principal_amount': 50000.00,
                'interest_rate': 7.0,
                'maturity_date': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
                'maturity_amount': 51750.00,
                'days_to_maturity': 180
            }
        ]
    },
    'AXIS': {
        'accounts': [
            {
                'account_number': '1111222233',
                'account_type': 'Savings',
                'balance': 200000.75,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            },
            {
                'account_number': '4444555566',
                'account_type': 'Salary',
                'balance': 150000.00,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            }
        ],
        'fixed_deposits': [
            {
                'fd_number': 'AXISFD001',
                'principal_amount': 200000.00,
                'interest_rate': 6.8,
                'maturity_date': (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d'),
                'maturity_amount': 227200.00,
                'days_to_maturity': 730
            }
        ]
    },
    'YES': {
        'accounts': [
            {
                'account_number': '7777888899',
                'account_type': 'Savings',
                'balance': 85000.25,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            }
        ],
        'fixed_deposits': [
            {
                'fd_number': 'YESFD001',
                'principal_amount': 150000.00,
                'interest_rate': 6.2,
                'maturity_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                'maturity_amount': 152325.00,
                'days_to_maturity': 90
            },
            {
                'fd_number': 'YESFD002',
                'principal_amount': 80000.00,
                'interest_rate': 6.0,
                'maturity_date': (datetime.now() + timedelta(days=270)).strftime('%Y-%m-%d'),
                'maturity_amount': 83600.00,
                'days_to_maturity': 270
            }
        ]
    },
    'HDFC': {
        'accounts': [
            {
                'account_number': '5555666677',
                'account_type': 'Savings',
                'balance': 300000.00,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            },
            {
                'account_number': '8888999900',
                'account_type': 'Current',
                'balance': 100000.00,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            },
            {
                'account_number': '1111222233',
                'account_type': 'PPF',
                'balance': 500000.00,
                'currency': 'INR',
                'last_updated': datetime.now().isoformat()
            }
        ],
        'fixed_deposits': [
            {
                'fd_number': 'HDFCFD001',
                'principal_amount': 300000.00,
                'interest_rate': 7.2,
                'maturity_date': (datetime.now() + timedelta(days=1095)).strftime('%Y-%m-%d'),
                'maturity_amount': 364800.00,
                'days_to_maturity': 1095
            },
            {
                'fd_number': 'HDFCFD002',
                'principal_amount': 100000.00,
                'interest_rate': 6.9,
                'maturity_date': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
                'maturity_amount': 103450.00,
                'days_to_maturity': 180
            }
        ]
    }
}

@app.route('/api/v1/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts for a bank"""
    bank = request.headers.get('X-Bank-Name', 'ICICI')
    if bank not in MOCK_DATA:
        return jsonify({'error': 'Bank not supported'}), 400
    
    return jsonify({
        'status': 'success',
        'data': {
            'accounts': MOCK_DATA[bank]['accounts']
        }
    })

@app.route('/api/v1/accounts/<account_id>/balance', methods=['GET'])
def get_account_balance(account_id):
    """Get balance for specific account"""
    bank = request.headers.get('X-Bank-Name', 'ICICI')
    if bank not in MOCK_DATA:
        return jsonify({'error': 'Bank not supported'}), 400
    
    # Find account by ID
    for account in MOCK_DATA[bank]['accounts']:
        if account['account_number'] == account_id:
            return jsonify({
                'status': 'success',
                'data': {
                    'account': account
                }
            })
    
    return jsonify({'error': 'Account not found'}), 404

@app.route('/api/v1/fixed-deposits', methods=['GET'])
def get_fixed_deposits():
    """Get all fixed deposits for a bank"""
    bank = request.headers.get('X-Bank-Name', 'ICICI')
    if bank not in MOCK_DATA:
        return jsonify({'error': 'Bank not supported'}), 400
    
    return jsonify({
        'status': 'success',
        'data': {
            'fixed_deposits': MOCK_DATA[bank]['fixed_deposits']
        }
    })

@app.route('/api/v1/accounts/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    """Get transactions for specific account"""
    bank = request.headers.get('X-Bank-Name', 'ICICI')
    if bank not in MOCK_DATA:
        return jsonify({'error': 'Bank not supported'}), 400
    
    # Generate mock transactions
    transactions = []
    for i in range(10):
        transactions.append({
            'transaction_id': f'TXN{random.randint(100000, 999999)}',
            'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'description': f'Transaction {i+1}',
            'amount': round(random.uniform(-5000, 10000), 2),
            'type': 'debit' if random.random() < 0.5 else 'credit',
            'balance': round(random.uniform(50000, 200000), 2)
        })
    
    return jsonify({
        'status': 'success',
        'data': {
            'transactions': transactions
        }
    })

@app.route('/api/v1/summary', methods=['GET'])
def get_summary():
    """Get summary for all banks"""
    summary = {
        'total_balance': 0,
        'total_fd_amount': 0,
        'total_accounts': 0,
        'total_fds': 0,
        'banks': []
    }
    
    for bank, data in MOCK_DATA.items():
        bank_summary = {
            'bank': bank,
            'total_balance': sum(acc['balance'] for acc in data['accounts']),
            'total_fd_amount': sum(fd['principal_amount'] for fd in data['fixed_deposits']),
            'account_count': len(data['accounts']),
            'fd_count': len(data['fixed_deposits'])
        }
        summary['banks'].append(bank_summary)
        summary['total_balance'] += bank_summary['total_balance']
        summary['total_fd_amount'] += bank_summary['total_fd_amount']
        summary['total_accounts'] += bank_summary['account_count']
        summary['total_fds'] += bank_summary['fd_count']
    
    return jsonify({
        'status': 'success',
        'data': summary
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Mock Bank API Server...")
    print("📊 Available endpoints:")
    print("  GET /api/v1/accounts - Get all accounts")
    print("  GET /api/v1/accounts/<id>/balance - Get account balance")
    print("  GET /api/v1/fixed-deposits - Get fixed deposits")
    print("  GET /api/v1/accounts/<id>/transactions - Get transactions")
    print("  GET /api/v1/summary - Get summary for all banks")
    print("  GET /health - Health check")
    print("\n🔧 Usage:")
    print("  Set X-Bank-Name header to: ICICI, AXIS, YES, or HDFC")
    print("  Example: curl -H 'X-Bank-Name: ICICI' http://localhost:5000/api/v1/accounts")
    print("\n🌐 Server running at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)