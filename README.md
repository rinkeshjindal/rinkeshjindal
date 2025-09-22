# India Bank Balance Checker

A secure Python application for checking bank balances and fixed deposits from major Indian banks.

## ⚠️ Important Security Notice

This application is designed to work with official bank APIs and secure authentication methods. It does NOT use web scraping or unauthorized access methods.

## Features

- Secure credential management
- Google Sheets integration for reporting
- Support for multiple Indian banks
- Fixed deposit tracking with maturity dates
- Automated reporting with date stamps
- Excel export functionality

## Supported Banks

- ICICI Bank
- Axis Bank
- Yes Bank
- HDFC Bank

## Prerequisites

1. Python 3.8 or higher
2. Google Cloud Platform account with Sheets API enabled
3. Bank account credentials (stored securely)
4. Chrome browser (for Selenium-based operations)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd india-bank-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Set up Google Sheets API:
   - Create a project in Google Cloud Console
   - Enable Google Sheets API
   - Download credentials JSON file
   - Place it in the project root as `credentials.json`

## Usage

1. Configure your bank credentials in the Excel file or environment variables
2. Run the main script:
```bash
python main.py
```

## Security

- All credentials are encrypted and stored securely
- No sensitive data is logged
- Uses official APIs where available
- Implements proper error handling

## Disclaimer

This tool is for personal use only. Users are responsible for complying with their bank's terms of service and applicable laws.