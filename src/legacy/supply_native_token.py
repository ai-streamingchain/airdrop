from web3 import Web3
from dotenv import load_dotenv
import os
import csv
import time

def read_wallets_from_csv(csv_file):
    """
    Read wallet addresses from CSV file
    """
    wallets = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:  # Ensure row has at least address
                wallets.append({
                    'no': row[0],
                    'address': row[1]
                })
    return wallets

def transfer_tokens(web3, from_wallet, to_address, amount_wei):
    """
    Transfer native tokens from main wallet to target address
    """
    try:
        # Get the nonce
        nonce = web3.eth.get_transaction_count(from_wallet.address)
        
        # Get the current gas price
        gas_price = web3.eth.gas_price
        
        # Build the transaction
        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': amount_wei,
            'gas': 21000,  # Standard gas limit for ETH transfers
            'gasPrice': gas_price,
            'chainId': web3.eth.chain_id
        }
        
        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, from_wallet.key)
        
        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt
    except Exception as e:
        print(f"Error in transfer: {str(e)}")
        return None

def main():
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get configuration from .env file
        main_wallet_address = os.getenv('MAIN_WALLET_ADDRESS')
        main_wallet_private_key = os.getenv('MAIN_WALLET_PRIVATE_KEY')
        token_amount = os.getenv('TOKEN_AMOUNT')
        wallets_file = os.getenv('WALLETS_FILE', 'wallets.csv')  # Default to wallets.csv if not specified
        web3_provider = os.getenv('WEB3_PROVIDER')
        
        # Validate environment variables
        if not all([main_wallet_address, main_wallet_private_key, token_amount, web3_provider]):
            print("Error: Missing required environment variables")
            print("Please ensure .env file contains:")
            print("MAIN_WALLET_ADDRESS=<address>")
            print("MAIN_WALLET_PRIVATE_KEY=<private_key>")
            print("TOKEN_AMOUNT=<amount_in_eth>")
            print("WEB3_PROVIDER=<your_web3_provider_url>")
            return
            
        try:
            token_amount = float(token_amount)
        except ValueError:
            print("Error: TOKEN_AMOUNT must be a valid number")
            return
            
        if token_amount <= 0:
            print("Error: TOKEN_AMOUNT must be a positive number")
            return
        
        # Initialize Web3
        web3 = Web3(Web3.HTTPProvider(web3_provider))
        if not web3.is_connected():
            print("Error: Could not connect to Ethereum network")
            return
            
        # Create main wallet account
        main_wallet = web3.eth.account.from_key(main_wallet_private_key)
        
        # Verify main wallet address matches
        if main_wallet.address.lower() != main_wallet_address.lower():
            print("Error: Main wallet address does not match private key")
            return
        
        # Read wallets from CSV
        print(f"\nReading wallets from {wallets_file}...")
        wallets = read_wallets_from_csv(wallets_file)
        
        if not wallets:
            print("Error: No wallets found in the CSV file")
            return
            
        print(f"Found {len(wallets)} wallets")
        
        # Convert token amount to Wei
        amount_wei = web3.to_wei(token_amount, 'ether')
        
        # Transfer tokens to each wallet
        print("\nStarting token transfers...")
        for i, wallet in enumerate(wallets, 1):
            print(f"\nTransferring to wallet {i}/{len(wallets)}")
            print(f"Address: {wallet['address']}")
            
            receipt = transfer_tokens(web3, main_wallet, wallet['address'], amount_wei)
            
            if receipt and receipt['status'] == 1:
                print(f"Transfer successful! Transaction hash: {receipt['transactionHash'].hex()}")
            else:
                print("Transfer failed!")
            
            # Add a small delay between transfers
            time.sleep(2)
        
        print("\nAll transfers completed!")
        print("\nIMPORTANT: Keep your private keys secure and never share them!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 