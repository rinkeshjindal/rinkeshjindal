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
    
    # Bank API Configuration
    ICICI_API_KEY = os.getenv('ICICI_API_KEY', '')
    AXIS_API_KEY = os.getenv('AXIS_API_KEY', '')
    YES_API_KEY = os.getenv('YES_API_KEY', '')
    HDFC_API_KEY = os.getenv('HDFC_API_KEY', '')
    
    # Security
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
    
    # File Paths
    CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'bank_credentials.xlsx')
    OUTPUT_DIR = 'output'
    LOGS_DIR = 'logs'
    
    # Bank URLs (for reference - not used for scraping)
    BANK_URLS = {
        'ICICI': 'https://www.icicibank.com',
        'AXIS': 'https://www.axisbank.com',
        'YES': 'https://www.yesbank.in',
        'HDFC': 'https://www.hdfcbank.com'
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