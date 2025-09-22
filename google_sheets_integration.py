"""
Google Sheets integration for storing bank balance reports.
"""
import os
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    """Manages Google Sheets integration for bank reports."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_file: str, sheet_id: str):
        """Initialize Google Sheets manager."""
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Sheets API."""
        try:
            creds = None
            token_file = 'token.json'
            
            # Load existing credentials
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            logger.error(f"Error authenticating with Google Sheets: {e}")
            raise
    
    def create_sheet_with_date(self, base_name: str = "India Bank Report") -> str:
        """Create a new sheet with today's date appended."""
        today = datetime.now().strftime("%Y-%m-%d")
        sheet_name = f"{base_name} {today}"
        
        try:
            # Create the sheet
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }
            
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=request_body
            ).execute()
            
            logger.info(f"Created new sheet: {sheet_name}")
            return sheet_name
            
        except HttpError as e:
            if e.resp.status == 400 and "already exists" in str(e):
                logger.info(f"Sheet {sheet_name} already exists")
                return sheet_name
            else:
                logger.error(f"Error creating sheet: {e}")
                raise
    
    def write_balance_report(self, balance_data: list, sheet_name: str):
        """Write current balance report to Google Sheets."""
        try:
            # Prepare headers
            headers = ['Bank', 'Account Number', 'Account Type', 'Current Balance', 'Last Updated']
            
            # Prepare data
            values = [headers]
            for bank_data in balance_data:
                for account in bank_data.get('accounts', []):
                    values.append([
                        bank_data['bank'],
                        account.get('account_number', 'N/A'),
                        account.get('account_type', 'N/A'),
                        account.get('balance', 'N/A'),
                        account.get('last_updated', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ])
            
            # Write to sheet
            range_name = f"{sheet_name}!A1:E{len(values)}"
            body = {'values': values}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Balance report written to {sheet_name}")
            
        except Exception as e:
            logger.error(f"Error writing balance report: {e}")
            raise
    
    def write_fd_report(self, fd_data: list, sheet_name: str):
        """Write fixed deposit report to Google Sheets."""
        try:
            # Prepare headers
            headers = ['Bank', 'FD Number', 'Principal Amount', 'Interest Rate', 'Maturity Date', 'Maturity Amount', 'Days to Maturity']
            
            # Prepare data
            values = [headers]
            for bank_data in fd_data:
                for fd in bank_data.get('fixed_deposits', []):
                    values.append([
                        bank_data['bank'],
                        fd.get('fd_number', 'N/A'),
                        fd.get('principal_amount', 'N/A'),
                        fd.get('interest_rate', 'N/A'),
                        fd.get('maturity_date', 'N/A'),
                        fd.get('maturity_amount', 'N/A'),
                        fd.get('days_to_maturity', 'N/A')
                    ])
            
            # Write to sheet (starting from column F)
            range_name = f"{sheet_name}!F1:L{len(values)}"
            body = {'values': values}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"FD report written to {sheet_name}")
            
        except Exception as e:
            logger.error(f"Error writing FD report: {e}")
            raise
    
    def format_sheet(self, sheet_name: str):
        """Apply formatting to the sheet."""
        try:
            requests = [
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': self._get_sheet_id(sheet_name),
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                },
                {
                    'autoResizeDimensions': {
                        'dimensions': {
                            'sheetId': self._get_sheet_id(sheet_name),
                            'dimension': 'COLUMNS',
                            'startIndex': 0,
                            'endIndex': 12
                        }
                    }
                }
            ]
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body={'requests': requests}
            ).execute()
            
            logger.info(f"Formatting applied to {sheet_name}")
            
        except Exception as e:
            logger.error(f"Error formatting sheet: {e}")
    
    def _get_sheet_id(self, sheet_name: str) -> int:
        """Get the sheet ID for a given sheet name."""
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            raise ValueError(f"Sheet {sheet_name} not found")
        except Exception as e:
            logger.error(f"Error getting sheet ID: {e}")
            raise
    
    def export_to_excel(self, sheet_name: str, output_path: str = None):
        """Export the sheet data to Excel format."""
        try:
            if not output_path:
                today = datetime.now().strftime("%Y%m%d")
                output_path = f"India_Bank_Report_{today}.xlsx"
            
            # Get all data from the sheet
            range_name = f"{sheet_name}!A:L"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.warning("No data found in sheet")
                return
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(values[1:], columns=values[0])
            df.to_excel(output_path, index=False)
            
            logger.info(f"Data exported to Excel: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise