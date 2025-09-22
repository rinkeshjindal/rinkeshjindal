"""
Reporting and data processing module for bank balance reports.
"""
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict
import os

logger = logging.getLogger(__name__)

class BankReportGenerator:
    """Generates comprehensive bank balance and FD reports."""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize the report generator."""
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def generate_balance_report(self, bank_data: List[Dict]) -> pd.DataFrame:
        """Generate current balance report from bank data."""
        try:
            balance_records = []
            
            for bank_info in bank_data:
                bank_name = bank_info.get('bank', 'Unknown')
                
                for account in bank_info.get('accounts', []):
                    balance_records.append({
                        'Bank': bank_name,
                        'Account Number': account.get('account_number', 'N/A'),
                        'Account Type': account.get('account_type', 'N/A'),
                        'Current Balance': account.get('balance', 0),
                        'Last Updated': account.get('last_updated', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            
            df = pd.DataFrame(balance_records)
            
            if not df.empty:
                # Sort by bank name and balance
                df = df.sort_values(['Bank', 'Current Balance'], ascending=[True, False])
                logger.info(f"Generated balance report with {len(df)} accounts")
            else:
                logger.warning("No account data found for balance report")
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating balance report: {e}")
            return pd.DataFrame()
    
    def generate_fd_report(self, bank_data: List[Dict]) -> pd.DataFrame:
        """Generate fixed deposit report from bank data."""
        try:
            fd_records = []
            
            for bank_info in bank_data:
                bank_name = bank_info.get('bank', 'Unknown')
                
                for fd in bank_info.get('fixed_deposits', []):
                    fd_records.append({
                        'Bank': bank_name,
                        'FD Number': fd.get('fd_number', 'N/A'),
                        'Principal Amount': fd.get('principal_amount', 0),
                        'Interest Rate': fd.get('interest_rate', 0),
                        'Maturity Date': fd.get('maturity_date', 'N/A'),
                        'Maturity Amount': fd.get('maturity_amount', 0),
                        'Days to Maturity': fd.get('days_to_maturity', 0)
                    })
            
            df = pd.DataFrame(fd_records)
            
            if not df.empty:
                # Sort by maturity date (soonest first)
                df = df.sort_values('Days to Maturity', ascending=True)
                logger.info(f"Generated FD report with {len(df)} fixed deposits")
            else:
                logger.warning("No FD data found for FD report")
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating FD report: {e}")
            return pd.DataFrame()
    
    def generate_summary_report(self, bank_data: List[Dict]) -> Dict:
        """Generate summary statistics."""
        try:
            total_balance = 0
            total_fd_amount = 0
            bank_count = len(bank_data)
            account_count = 0
            fd_count = 0
            
            for bank_info in bank_data:
                # Count accounts and sum balances
                for account in bank_info.get('accounts', []):
                    account_count += 1
                    total_balance += float(account.get('balance', 0))
                
                # Count FDs and sum amounts
                for fd in bank_info.get('fixed_deposits', []):
                    fd_count += 1
                    total_fd_amount += float(fd.get('principal_amount', 0))
            
            summary = {
                'Report Generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Total Banks': bank_count,
                'Total Accounts': account_count,
                'Total Balance': total_balance,
                'Total FD Count': fd_count,
                'Total FD Amount': total_fd_amount,
                'Total Portfolio Value': total_balance + total_fd_amount
            }
            
            logger.info("Generated summary report")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return {}
    
    def save_reports_to_excel(self, balance_df: pd.DataFrame, fd_df: pd.DataFrame, 
                            summary: Dict, filename: str = None) -> str:
        """Save all reports to an Excel file."""
        try:
            if not filename:
                today = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"India_Bank_Report_{today}.xlsx"
            
            filepath = os.path.join(self.output_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Summary sheet
                if summary:
                    summary_df = pd.DataFrame([summary])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Balance report
                if not balance_df.empty:
                    balance_df.to_excel(writer, sheet_name='Current Balances', index=False)
                
                # FD report
                if not fd_df.empty:
                    fd_df.to_excel(writer, sheet_name='Fixed Deposits', index=False)
            
            logger.info(f"Reports saved to Excel: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving reports to Excel: {e}")
            raise
    
    def format_currency(self, amount: float) -> str:
        """Format amount as Indian currency."""
        try:
            return f"₹{amount:,.2f}"
        except:
            return f"₹{amount}"
    
    def generate_html_report(self, balance_df: pd.DataFrame, fd_df: pd.DataFrame, 
                           summary: Dict, filename: str = None) -> str:
        """Generate an HTML report."""
        try:
            if not filename:
                today = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"India_Bank_Report_{today}.html"
            
            filepath = os.path.join(self.output_dir, filename)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>India Bank Report - {datetime.now().strftime("%Y-%m-%d")}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2 {{ color: #2c3e50; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; }}
                    .currency {{ text-align: right; }}
                </style>
            </head>
            <body>
                <h1>India Bank Report - {datetime.now().strftime("%Y-%m-%d")}</h1>
                
                <div class="summary">
                    <h2>Summary</h2>
                    <p><strong>Report Generated:</strong> {summary.get('Report Generated', 'N/A')}</p>
                    <p><strong>Total Banks:</strong> {summary.get('Total Banks', 0)}</p>
                    <p><strong>Total Accounts:</strong> {summary.get('Total Accounts', 0)}</p>
                    <p><strong>Total Balance:</strong> {self.format_currency(summary.get('Total Balance', 0))}</p>
                    <p><strong>Total FD Count:</strong> {summary.get('Total FD Count', 0)}</p>
                    <p><strong>Total FD Amount:</strong> {self.format_currency(summary.get('Total FD Amount', 0))}</p>
                    <p><strong>Total Portfolio Value:</strong> {self.format_currency(summary.get('Total Portfolio Value', 0))}</p>
                </div>
                
                <h2>Current Account Balances</h2>
                {balance_df.to_html(index=False, classes='currency') if not balance_df.empty else '<p>No account data available</p>'}
                
                <h2>Fixed Deposits (Sorted by Maturity Date)</h2>
                {fd_df.to_html(index=False, classes='currency') if not fd_df.empty else '<p>No FD data available</p>'}
                
            </body>
            </html>
            """
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            raise