"""
Development version of India Bank Checker using Mock APIs
This allows you to build and test your application without official API approval
"""
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Import our modules
from config import Config
from secure_credentials import SecureCredentialManager
from mock_bank_integration import MockBankAPIFactory
from google_sheets_integration import GoogleSheetsManager
from reporting import BankReportGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bank_checker_dev.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class IndiaBankCheckerDev:
    """Development version of India Bank Checker using Mock APIs."""
    
    def __init__(self):
        """Initialize the development application."""
        self.config = Config()
        self.credential_manager = None
        self.sheets_manager = None
        self.report_generator = BankReportGenerator()
        
        # Ensure required directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        self.setup_managers()
    
    def setup_managers(self):
        """Set up credential and Google Sheets managers."""
        try:
            # For development, we'll use mock credentials
            logger.info("Setting up development environment with mock APIs")
            
            # Initialize credential manager
            self.credential_manager = SecureCredentialManager(
                self.config.ENCRYPTION_KEY or "dev_encryption_key_32_chars"
            )
            
            # Initialize Google Sheets manager (optional for development)
            try:
                if self.config.GOOGLE_SHEET_ID:
                    self.sheets_manager = GoogleSheetsManager(
                        self.config.GOOGLE_SHEETS_CREDENTIALS_FILE,
                        self.config.GOOGLE_SHEET_ID
                    )
                    logger.info("Google Sheets integration enabled")
                else:
                    logger.info("Google Sheets integration disabled (no SHEET_ID configured)")
            except Exception as e:
                logger.warning(f"Google Sheets integration disabled: {e}")
            
            logger.info("Development managers initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up development managers: {e}")
            raise
    
    def create_mock_credentials(self):
        """Create mock credentials for development."""
        try:
            logger.info("Creating mock credentials for development")
            
            # Create mock credentials for each bank
            mock_credentials = {
                'ICICI': {'username': 'mock_icici_user', 'password': 'mock_icici_pass'},
                'AXIS': {'username': 'mock_axis_user', 'password': 'mock_axis_pass'},
                'YES': {'username': 'mock_yes_user', 'password': 'mock_yes_pass'},
                'HDFC': {'username': 'mock_hdfc_user', 'password': 'mock_hdfc_pass'}
            }
            
            for bank, creds in mock_credentials.items():
                self.credential_manager.store_credential(
                    bank, creds['username'], creds['password']
                )
            
            logger.info("Mock credentials created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating mock credentials: {e}")
            return False
    
    def get_bank_data(self) -> List[Dict]:
        """Get data from all banks using mock APIs."""
        bank_data = []
        supported_banks = ['ICICI', 'AXIS', 'YES', 'HDFC']
        
        for bank in supported_banks:
            try:
                logger.info(f"Processing {bank} Bank using mock API...")
                
                # Get credentials for this bank
                credentials = self.credential_manager.get_bank_credentials(bank)
                
                if not credentials:
                    logger.warning(f"No credentials found for {bank} Bank")
                    continue
                
                # Create mock bank API instance
                bank_api = MockBankAPIFactory.create_mock_bank_api(
                    bank,
                    credentials['username'],
                    credentials['password']
                )
                
                # Get bank data
                data = bank_api.get_bank_data()
                bank_data.append(data)
                
                logger.info(f"Successfully processed {bank} Bank using mock API")
                
            except Exception as e:
                logger.error(f"Error processing {bank} Bank: {e}")
                # Add empty data for failed banks
                bank_data.append({
                    'bank': bank,
                    'accounts': [],
                    'fixed_deposits': []
                })
        
        return bank_data
    
    def generate_reports(self, bank_data: List[Dict]) -> tuple:
        """Generate all reports from bank data."""
        try:
            logger.info("Generating reports...")
            
            # Generate balance report
            balance_df = self.report_generator.generate_balance_report(bank_data)
            
            # Generate FD report
            fd_df = self.report_generator.generate_fd_report(bank_data)
            
            # Generate summary
            summary = self.report_generator.generate_summary_report(bank_data)
            
            logger.info("Reports generated successfully")
            return balance_df, fd_df, summary
            
        except Exception as e:
            logger.error(f"Error generating reports: {e}")
            raise
    
    def save_to_google_sheets(self, balance_df, fd_df, summary):
        """Save reports to Google Sheets (if configured)."""
        if not self.sheets_manager:
            logger.info("Google Sheets integration not configured, skipping...")
            return
        
        try:
            logger.info("Saving reports to Google Sheets...")
            
            # Create sheet with today's date
            sheet_name = self.sheets_manager.create_sheet_with_date(
                f"{self.config.SHEET_NAME} (Dev)"
            )
            
            # Write balance report
            if not balance_df.empty:
                balance_data = [{
                    'bank': bank,
                    'accounts': [row.to_dict() for _, row in balance_df[balance_df['Bank'] == bank].iterrows()]
                } for bank in balance_df['Bank'].unique()]
                self.sheets_manager.write_balance_report(balance_data, sheet_name)
            
            # Write FD report
            if not fd_df.empty:
                fd_data = [{
                    'bank': bank,
                    'fixed_deposits': [row.to_dict() for _, row in fd_df[fd_df['Bank'] == bank].iterrows()]
                } for bank in fd_df['Bank'].unique()]
                self.sheets_manager.write_fd_report(fd_data, sheet_name)
            
            # Apply formatting
            self.sheets_manager.format_sheet(sheet_name)
            
            logger.info(f"Reports saved to Google Sheets: {sheet_name}")
            
        except Exception as e:
            logger.error(f"Error saving to Google Sheets: {e}")
            raise
    
    def save_to_excel(self, balance_df, fd_df, summary):
        """Save reports to Excel file."""
        try:
            logger.info("Saving reports to Excel...")
            
            filepath = self.report_generator.save_reports_to_excel(
                balance_df, fd_df, summary
            )
            
            logger.info(f"Reports saved to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving to Excel: {e}")
            raise
    
    def run(self):
        """Run the complete bank checking process using mock APIs."""
        try:
            logger.info("Starting India Bank Checker (Development Mode)...")
            print("🚀 Starting India Bank Checker (Development Mode)")
            print("📊 Using Mock APIs - No official approval required")
            print("=" * 60)
            
            # Create mock credentials
            if not self.create_mock_credentials():
                logger.error("Failed to create mock credentials")
                return False
            
            # Get bank data
            bank_data = self.get_bank_data()
            
            if not bank_data:
                logger.error("No bank data retrieved")
                return False
            
            # Generate reports
            balance_df, fd_df, summary = self.generate_reports(bank_data)
            
            # Save to Google Sheets (if configured)
            try:
                self.save_to_google_sheets(balance_df, fd_df, summary)
            except Exception as e:
                logger.warning(f"Failed to save to Google Sheets: {e}")
            
            # Save to Excel
            excel_file = self.save_to_excel(balance_df, fd_df, summary)
            
            # Print summary
            self.print_summary(summary)
            
            logger.info("India Bank Checker (Development Mode) completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error running India Bank Checker (Development Mode): {e}")
            return False
    
    def print_summary(self, summary: Dict):
        """Print summary to console."""
        print("\n" + "="*60)
        print("INDIA BANK REPORT SUMMARY (DEVELOPMENT MODE)")
        print("="*60)
        print(f"Report Generated: {summary.get('Report Generated', 'N/A')}")
        print(f"Total Banks: {summary.get('Total Banks', 0)}")
        print(f"Total Accounts: {summary.get('Total Accounts', 0)}")
        print(f"Total Balance: ₹{summary.get('Total Balance', 0):,.2f}")
        print(f"Total FD Count: {summary.get('Total FD Count', 0)}")
        print(f"Total FD Amount: ₹{summary.get('Total FD Amount', 0):,.2f}")
        print(f"Total Portfolio Value: ₹{summary.get('Total Portfolio Value', 0):,.2f}")
        print("="*60)
        print("💡 This is development data - not real bank information")
        print("🔧 Use this to build your prototype while waiting for API approval")

def main():
    """Main entry point for development mode."""
    try:
        print("🧪 India Bank Checker - Development Mode")
        print("📊 Using Mock APIs for development and testing")
        print("🚀 No official API approval required")
        print("=" * 60)
        
        app = IndiaBankCheckerDev()
        success = app.run()
        
        if success:
            print("\n✅ Development mode completed successfully!")
            print("📁 Check the 'output' folder for Excel reports")
            print("🔧 Use this prototype to demonstrate your application")
            print("📋 Submit this prototype with your official API applications")
        else:
            print("\n❌ Development mode failed. Check the logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()