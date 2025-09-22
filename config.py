"""
Configuration settings for the India Bank Checker application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
    
    # ICICI Bank API Configuration
    ICICI_API_KEY = os.getenv('ICICI_API_KEY', '')
    ICICI_CLIENT_ID = os.getenv('ICICI_CLIENT_ID', '')
    ICICI_CLIENT_SECRET = os.getenv('ICICI_CLIENT_SECRET', '')
    ICICI_CUSTOMER_ID = os.getenv('ICICI_CUSTOMER_ID', '')
    
    # Axis Bank API Configuration
    AXIS_API_KEY = os.getenv('AXIS_API_KEY', '')
    AXIS_CLIENT_ID = os.getenv('AXIS_CLIENT_ID', '')
    AXIS_CLIENT_SECRET = os.getenv('AXIS_CLIENT_SECRET', '')
    AXIS_MERCHANT_ID = os.getenv('AXIS_MERCHANT_ID', '')
    
    # Yes Bank API Configuration
    YES_API_KEY = os.getenv('YES_API_KEY', '')
    YES_CLIENT_ID = os.getenv('YES_CLIENT_ID', '')
    YES_CLIENT_SECRET = os.getenv('YES_CLIENT_SECRET', '')
    YES_MERCHANT_CODE = os.getenv('YES_MERCHANT_CODE', '')
    
    # HDFC Bank API Configuration
    HDFC_API_KEY = os.getenv('HDFC_API_KEY', '')
    HDFC_CLIENT_ID = os.getenv('HDFC_CLIENT_ID', '')
    HDFC_CLIENT_SECRET = os.getenv('HDFC_CLIENT_SECRET', '')
    HDFC_MERCHANT_ID = os.getenv('HDFC_MERCHANT_ID', '')
    
    # Security
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
    
    # File Paths
    CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'bank_credentials.xlsx')
    OUTPUT_DIR = 'output'
    LOGS_DIR = 'logs'
    
    # Bank API URLs
    BANK_API_URLS = {
        'ICICI': 'https://api.icicibank.com',
        'AXIS': 'https://api.axisbank.com',
        'YES': 'https://api.yesbank.in',
        'HDFC': 'https://api.hdfcbank.com'
    }
    
    # Bank API Scopes
    BANK_API_SCOPES = {
        'ICICI': ['account.read', 'transaction.read', 'fd.read'],
        'AXIS': ['account.read', 'transaction.read', 'fd.read'],
        'YES': ['account.read', 'transaction.read', 'fd.read'],
        'HDFC': ['account.read', 'transaction.read', 'fd.read']
    }
    
    # Google Sheets Configuration
    SHEET_NAME = 'India Bank Report'
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        required_vars = [
            'GOOGLE_SHEET_ID',
            'ENCRYPTION_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_bank_api_config(cls, bank_name: str) -> dict:
        """Get API configuration for a specific bank."""
        bank_name = bank_name.upper()
        
        if bank_name == 'ICICI':
            return {
                'api_key': cls.ICICI_API_KEY,
                'client_id': cls.ICICI_CLIENT_ID,
                'client_secret': cls.ICICI_CLIENT_SECRET,
                'customer_id': cls.ICICI_CUSTOMER_ID,
                'base_url': cls.BANK_API_URLS['ICICI'],
                'scopes': cls.BANK_API_SCOPES['ICICI']
            }
        elif bank_name == 'AXIS':
            return {
                'api_key': cls.AXIS_API_KEY,
                'client_id': cls.AXIS_CLIENT_ID,
                'client_secret': cls.AXIS_CLIENT_SECRET,
                'merchant_id': cls.AXIS_MERCHANT_ID,
                'base_url': cls.BANK_API_URLS['AXIS'],
                'scopes': cls.BANK_API_SCOPES['AXIS']
            }
        elif bank_name == 'YES':
            return {
                'api_key': cls.YES_API_KEY,
                'client_id': cls.YES_CLIENT_ID,
                'client_secret': cls.YES_CLIENT_SECRET,
                'merchant_code': cls.YES_MERCHANT_CODE,
                'base_url': cls.BANK_API_URLS['YES'],
                'scopes': cls.BANK_API_SCOPES['YES']
            }
        elif bank_name == 'HDFC':
            return {
                'api_key': cls.HDFC_API_KEY,
                'client_id': cls.HDFC_CLIENT_ID,
                'client_secret': cls.HDFC_CLIENT_SECRET,
                'merchant_id': cls.HDFC_MERCHANT_ID,
                'base_url': cls.BANK_API_URLS['HDFC'],
                'scopes': cls.BANK_API_SCOPES['HDFC']
            }
        else:
            raise ValueError(f"Unsupported bank: {bank_name}")