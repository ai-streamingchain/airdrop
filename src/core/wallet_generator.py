"""
Wallet generation module for creating new BSC/Ethereum wallets
"""

from web3 import Web3
import csv
from datetime import datetime
import os

class WalletGenerator:
    """Wallet generation class"""
    
    def __init__(self):
        self.generated_wallets = []
    
    def generate_wallets(self, num_wallets, progress_callback=None):
        """Generate specified number of wallets"""
        wallets = []
        
        for i in range(num_wallets):
            # Generate a new account
            account = Web3().eth.account.create()
            
            wallet_info = {
                'no': i + 1,
                'address': account.address,
                'private_key': account.key.hex()
            }
            wallets.append(wallet_info)
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(f"Generated wallet {i+1}/{num_wallets}: {account.address}")
        
        self.generated_wallets = wallets
        return wallets
    
    def save_wallets_to_csv(self, filename=None):
        """Save generated wallets to CSV file"""
        if not self.generated_wallets:
            raise Exception("No wallets generated yet!")
        
        # Generate filename with current date and time if not provided
        if not filename:
            current_time = datetime.now()
            filename = f"wallets_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}_{current_time.second}.csv"
        
        try:
            # Create wallets directory if it doesn't exist
            os.makedirs('wallets', exist_ok=True)
            
            # Full path for the file
            filepath = os.path.join('wallets', filename)
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                for wallet in self.generated_wallets:
                    writer.writerow([wallet['no'], wallet['address'], wallet['private_key']])
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Error saving wallets to CSV: {str(e)}")
    
    def get_generated_wallets(self):
        """Get the list of generated wallets"""
        return self.generated_wallets
    
    def clear_generated_wallets(self):
        """Clear the generated wallets list"""
        self.generated_wallets = []
