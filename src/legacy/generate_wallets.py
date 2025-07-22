from web3 import Web3
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

def generate_wallets(num_wallets):
    """
    Generate specified number of Ethereum wallets
    Returns a list of dictionaries containing wallet information
    """
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
    
    return wallets

def save_wallets_to_csv(wallets):
    """
    Save wallet information to a CSV file without headers in the wallets folder
    with date-based filename
    """
    # Create wallets folder if it doesn't exist
    os.makedirs('wallets', exist_ok=True)
    
    # Generate filename with current date and time
    current_time = datetime.now()
    filename = f"wallets_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}_{current_time.second}.csv"
    filepath = os.path.join('wallets', filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        for wallet in wallets:
            writer.writerow([wallet['no'], wallet['address'], wallet['private_key']])
    
    return filepath

def main():
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get number of wallets from .env file
        num_wallets = os.getenv('NUMBER_OF_WALLETS')
        
        if num_wallets is None:
            print("Error: NUMBER_OF_WALLETS not found in .env file")
            print("Please create a .env file with NUMBER_OF_WALLETS=<number>")
            return
            
        try:
            num_wallets = int(num_wallets)
        except ValueError:
            print("Error: NUMBER_OF_WALLETS in .env file must be a valid number")
            return
        
        if num_wallets <= 0:
            print("Error: NUMBER_OF_WALLETS must be a positive number")
            return
        
        # Generate wallets
        print(f"\nGenerating {num_wallets} wallets...")
        wallets = generate_wallets(num_wallets)
        
        # Save to CSV file
        filepath = save_wallets_to_csv(wallets)
        
        print(f"\nSuccessfully generated {num_wallets} wallets!")
        print(f"Wallet information has been saved to: {filepath}")
        
        # Display first wallet as example
        print("\nExample wallet (first one):")
        print(f"No: {wallets[0]['no']}")
        print(f"Address: {wallets[0]['address']}")
        print(f"Private Key: {wallets[0]['private_key']}")
        
        print("\nIMPORTANT: Keep your private keys secure and never share them!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 