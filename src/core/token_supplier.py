"""
Token supplier module for distributing native tokens to multiple wallets
"""

import csv
import time

try:
    from .blockchain import BSCBlockchain
except ImportError:
    from blockchain import BSCBlockchain

class TokenSupplier:
    """Token supplier class for distributing native tokens"""
    
    def __init__(self):
        self.blockchain = BSCBlockchain()
    
    def connect_to_network(self):
        """Connect to BSC network"""
        return self.blockchain.connect()
    
    def read_wallets_from_csv(self, csv_file):
        """Read wallet addresses from CSV file"""
        wallets = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:  # Ensure row has at least address
                        wallets.append({
                            'no': row[0],
                            'address': row[1]
                        })
        except FileNotFoundError:
            raise Exception(f"CSV file {csv_file} not found")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
        
        return wallets
    
    def supply_tokens_to_wallets(self, main_wallet_private_key, wallets, token_amount, progress_callback=None):
        """Supply native tokens to multiple wallets"""
        if not self.blockchain.connected:
            raise Exception("Not connected to BSC network")
        
        try:
            # Create main wallet account from private key
            main_wallet = self.blockchain.web3.eth.account.from_key(main_wallet_private_key)
            
            # Convert token amount to Wei
            amount_wei = self.blockchain.web3.to_wei(token_amount, 'ether')
            
            successful_transfers = 0
            failed_transfers = 0
            results = []
            
            for i, wallet in enumerate(wallets, 1):
                try:
                    if progress_callback:
                        progress_callback(f"Transferring to wallet {i}/{len(wallets)}: {wallet['address']}")
                    
                    receipt = self.blockchain.transfer_native_token(
                        main_wallet, 
                        wallet['address'], 
                        amount_wei
                    )
                    
                    if receipt and receipt['status'] == 1:
                        successful_transfers += 1
                        result = {
                            'wallet_no': wallet['no'],
                            'address': wallet['address'],
                            'status': 'success',
                            'tx_hash': receipt['transactionHash'].hex(),
                            'amount': token_amount
                        }
                        if progress_callback:
                            progress_callback(f"✓ Transfer successful! TX: {receipt['transactionHash'].hex()}")
                    else:
                        failed_transfers += 1
                        result = {
                            'wallet_no': wallet['no'],
                            'address': wallet['address'],
                            'status': 'failed',
                            'tx_hash': None,
                            'amount': token_amount,
                            'error': 'Transaction failed'
                        }
                        if progress_callback:
                            progress_callback(f"✗ Transfer failed!")
                    
                    results.append(result)
                    
                    # Add a small delay between transfers to avoid rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    failed_transfers += 1
                    result = {
                        'wallet_no': wallet['no'],
                        'address': wallet['address'],
                        'status': 'failed',
                        'tx_hash': None,
                        'amount': token_amount,
                        'error': str(e)
                    }
                    results.append(result)
                    
                    if progress_callback:
                        progress_callback(f"✗ Error transferring to {wallet['address']}: {str(e)}")
            
            # Summary
            summary = {
                'total_wallets': len(wallets),
                'successful_transfers': successful_transfers,
                'failed_transfers': failed_transfers,
                'total_amount_distributed': successful_transfers * token_amount,
                'results': results
            }
            
            return summary
            
        except Exception as e:
            raise Exception(f"Error during token distribution: {str(e)}")
    
    def validate_main_wallet(self, main_wallet_address, main_wallet_private_key):
        """Validate that the main wallet address matches the private key"""
        try:
            main_wallet = self.blockchain.web3.eth.account.from_key(main_wallet_private_key)
            return main_wallet.address.lower() == main_wallet_address.lower()
        except Exception:
            return False
    
    def get_main_wallet_balance(self, main_wallet_address):
        """Get the balance of the main wallet"""
        if not self.blockchain.connected:
            raise Exception("Not connected to BSC network")
        
        return self.blockchain.get_bnb_balance(main_wallet_address)
