"""
Main application for India Bank Balance Checker.
"""
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Import our modules
from config import Config
from secure_credentials import SecureCredentialManager
from bank_integration import BankAPIFactory
from google_sheets_integration import GoogleSheetsManager
from reporting import BankReportGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bank_checker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class IndiaBankChecker:
    """Main application class for India Bank Checker."""
    
    def __init__(self):
        """Initialize the application."""
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
            # Validate configuration
            self.config.validate_config()
            
            # Initialize credential manager
            self.credential_manager = SecureCredentialManager(
                self.config.ENCRYPTION_KEY
            )
            
            # Initialize Google Sheets manager
            self.sheets_manager = GoogleSheetsManager(
                self.config.GOOGLE_SHEETS_CREDENTIALS_FILE,
                self.config.GOOGLE_SHEET_ID
            )
            
            logger.info("Managers initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up managers: {e}")
            raise
    
    def load_credentials_from_excel(self, excel_file: str = None):
        """Load credentials from Excel file."""
        try:
            file_path = excel_file or self.config.CREDENTIALS_FILE
            
            if not os.path.exists(file_path):
                logger.info(f"Creating sample credentials file: {file_path}")
                self.credential_manager.create_sample_excel(file_path)
                logger.info("Please update the credentials file with your actual bank details")
                return False
            
            self.credential_manager.load_from_excel(file_path)
            logger.info("Credentials loaded from Excel file")
            return True
            
        except Exception as e:
            logger.error(f"Error loading credentials from Excel: {e}")
            return False
    
    def get_bank_data(self) -> List[Dict]:
        """Get data from all configured banks."""
        bank_data = []
        supported_banks = ['ICICI', 'AXIS', 'YES', 'HDFC']
        
        for bank in supported_banks:
            try:
                logger.info(f"Processing {bank} Bank...")
                
                # Get credentials for this bank
                credentials = self.credential_manager.get_bank_credentials(bank)
                
                if not credentials:
                    logger.warning(f"No credentials found for {bank} Bank")
                    continue
                
                # Get API key if available
                api_key = getattr(self.config, f"{bank}_API_KEY", None)
                
                # Create bank API instance
                bank_api = BankAPIFactory.create_bank_api(
                    bank,
                    credentials['username'],
                    credentials['password'],
                    api_key
                )
                
                # Get bank data
                data = bank_api.get_bank_data()
                bank_data.append(data)
                
                logger.info(f"Successfully processed {bank} Bank")
                
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
        """Save reports to Google Sheets."""
        try:
            logger.info("Saving reports to Google Sheets...")
            
            # Create sheet with today's date
            sheet_name = self.sheets_manager.create_sheet_with_date(
                self.config.SHEET_NAME
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
    
    def run(self, excel_file: str = None):
        """Run the complete bank checking process."""
        try:
            logger.info("Starting India Bank Checker...")
            
            # Load credentials
            if not self.load_credentials_from_excel(excel_file):
                logger.error("Failed to load credentials. Please check the Excel file.")
                return False
            
            # Get bank data
            bank_data = self.get_bank_data()
            
            if not bank_data:
                logger.error("No bank data retrieved")
                return False
            
            # Generate reports
            balance_df, fd_df, summary = self.generate_reports(bank_data)
            
            # Save to Google Sheets
            try:
                self.save_to_google_sheets(balance_df, fd_df, summary)
            except Exception as e:
                logger.warning(f"Failed to save to Google Sheets: {e}")
            
            # Save to Excel
            excel_file = self.save_to_excel(balance_df, fd_df, summary)
            
            # Print summary
            self.print_summary(summary)
            
            logger.info("India Bank Checker completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error running India Bank Checker: {e}")
            return False
    
    def print_summary(self, summary: Dict):
        """Print summary to console."""
        print("\n" + "="*50)
        print("INDIA BANK REPORT SUMMARY")
        print("="*50)
        print(f"Report Generated: {summary.get('Report Generated', 'N/A')}")
        print(f"Total Banks: {summary.get('Total Banks', 0)}")
        print(f"Total Accounts: {summary.get('Total Accounts', 0)}")
        print(f"Total Balance: ₹{summary.get('Total Balance', 0):,.2f}")
        print(f"Total FD Count: {summary.get('Total FD Count', 0)}")
        print(f"Total FD Amount: ₹{summary.get('Total FD Amount', 0):,.2f}")
        print(f"Total Portfolio Value: ₹{summary.get('Total Portfolio Value', 0):,.2f}")
        print("="*50)

def main():
    """Main entry point."""
    try:
        app = IndiaBankChecker()
        success = app.run()
        
        if success:
            print("\n✅ Bank checking completed successfully!")
            print("Check the 'output' folder for Excel reports and Google Sheets for online reports.")
        else:
            print("\n❌ Bank checking failed. Check the logs for details.")
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