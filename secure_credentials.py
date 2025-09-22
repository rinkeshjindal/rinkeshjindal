"""
Secure credential management system for bank credentials.
"""
import os
import pandas as pd
from cryptography.fernet import Fernet
import keyring
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SecureCredentialManager:
    """Manages bank credentials securely using encryption and keyring."""
    
    def __init__(self, encryption_key: str = None):
        """Initialize the credential manager."""
        self.encryption_key = encryption_key or os.getenv('ENCRYPTION_KEY')
        if not self.encryption_key:
            raise ValueError("Encryption key is required")
        
        # Ensure encryption key is 32 bytes for Fernet
        if len(self.encryption_key) != 32:
            self.encryption_key = self.encryption_key[:32].ljust(32, '0')
        
        self.cipher_suite = Fernet(self.encryption_key.encode())
        self.service_name = "IndiaBankChecker"
    
    def encrypt_credential(self, credential: str) -> str:
        """Encrypt a credential string."""
        try:
            encrypted = self.cipher_suite.encrypt(credential.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Error encrypting credential: {e}")
            raise
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """Decrypt a credential string."""
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_credential.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error decrypting credential: {e}")
            raise
    
    def store_credential(self, bank: str, username: str, password: str) -> None:
        """Store bank credentials securely."""
        try:
            # Encrypt credentials
            encrypted_username = self.encrypt_credential(username)
            encrypted_password = self.encrypt_credential(password)
            
            # Store in keyring
            keyring.set_password(
                self.service_name, 
                f"{bank}_username", 
                encrypted_username
            )
            keyring.set_password(
                self.service_name, 
                f"{bank}_password", 
                encrypted_password
            )
            
            logger.info(f"Credentials stored securely for {bank}")
        except Exception as e:
            logger.error(f"Error storing credentials for {bank}: {e}")
            raise
    
    def get_credential(self, bank: str, credential_type: str) -> Optional[str]:
        """Retrieve a specific credential."""
        try:
            encrypted_credential = keyring.get_password(
                self.service_name, 
                f"{bank}_{credential_type}"
            )
            
            if encrypted_credential:
                return self.decrypt_credential(encrypted_credential)
            return None
        except Exception as e:
            logger.error(f"Error retrieving {credential_type} for {bank}: {e}")
            return None
    
    def get_bank_credentials(self, bank: str) -> Dict[str, str]:
        """Get all credentials for a specific bank."""
        credentials = {}
        for cred_type in ['username', 'password']:
            cred = self.get_credential(bank, cred_type)
            if cred:
                credentials[cred_type] = cred
        
        return credentials
    
    def load_from_excel(self, file_path: str) -> None:
        """Load credentials from Excel file and store them securely."""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Credentials file not found: {file_path}")
                return
            
            df = pd.read_excel(file_path)
            
            # Expected columns: Bank, Username, Password
            required_columns = ['Bank', 'Username', 'Password']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Excel file must contain columns: {required_columns}")
            
            for _, row in df.iterrows():
                bank = row['Bank'].upper()
                username = str(row['Username'])
                password = str(row['Password'])
                
                if username and password and username != 'nan' and password != 'nan':
                    self.store_credential(bank, username, password)
                    logger.info(f"Loaded credentials for {bank}")
            
        except Exception as e:
            logger.error(f"Error loading credentials from Excel: {e}")
            raise
    
    def create_sample_excel(self, file_path: str) -> None:
        """Create a sample Excel file with the required format."""
        sample_data = {
            'Bank': ['ICICI', 'AXIS', 'YES', 'HDFC'],
            'Username': ['your_username_1', 'your_username_2', 'your_username_3', 'your_username_4'],
            'Password': ['your_password_1', 'your_password_2', 'your_password_3', 'your_password_4']
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel(file_path, index=False)
        logger.info(f"Sample credentials file created: {file_path}")
    
    def list_stored_banks(self) -> list:
        """List all banks with stored credentials."""
        banks = []
        for bank in ['ICICI', 'AXIS', 'YES', 'HDFC']:
            if self.get_credential(bank, 'username'):
                banks.append(bank)
        return banks
    
    def delete_credentials(self, bank: str) -> None:
        """Delete stored credentials for a specific bank."""
        try:
            keyring.delete_password(self.service_name, f"{bank}_username")
            keyring.delete_password(self.service_name, f"{bank}_password")
            logger.info(f"Credentials deleted for {bank}")
        except Exception as e:
            logger.error(f"Error deleting credentials for {bank}: {e}")