from web3 import Web3
from dotenv import load_dotenv
import os
import csv
import json

# BSC Network Configuration
BSC_RPC_URL = "https://bsc-dataseed1.binance.org/"
BSC_CHAIN_ID = 56

# USDC Contract Address on BSC (USDC-BSC)
USDC_BSC_CONTRACT = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
USDT_BSC_CONTRACT = "0x55d398326f99059ff775485246999027b3197955"

SPECIAL_WALLETS = [
    "0xBFe3A307dbADBd4dF9146EE5E694A268C4758141",
    "0xF791479FBDb9d385DCA288229Bd7269Ca7325432"
]

# Standard ERC20 ABI for balance checking
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

def get_bnb_balance(web3, address):
    """
    Get BNB balance for a given address
    """
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_bnb = web3.from_wei(balance_wei, 'ether')
        return float(balance_bnb)
    except Exception as e:
        print(f"Error getting BNB balance for {address}: {str(e)}")
        return 0.0

def get_token_balance(web3, address, token_contract, token_name):
    """
    Get token balance for a given address
    """
    try:
        # Get balance in smallest unit
        balance_raw = token_contract.functions.balanceOf(address).call()

        # Get decimals for proper conversion
        decimals = token_contract.functions.decimals().call()

        # Convert to human readable format
        balance_token = balance_raw / (10 ** decimals)
        return float(balance_token)
    except Exception as e:
        print(f"Error getting {token_name} balance for {address}: {str(e)}")
        return 0.0

def read_wallets_from_csv(csv_file):
    """
    Read wallet addresses from CSV file
    """
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
        print(f"Error: {csv_file} not found")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    
    return wallets

def check_single_wallet_balance(web3, usdc_contract, usdt_contract, address):
    """
    Check BNB, USDC, and USDT balance for a single wallet
    """
    bnb_balance = get_bnb_balance(web3, address)
    usdc_balance = get_token_balance(web3, address, usdc_contract, "USDC")
    usdt_balance = get_token_balance(web3, address, usdt_contract, "USDT")

    return {
        'address': address,
        'bnb_balance': bnb_balance,
        'usdc_balance': usdc_balance,
        'usdt_balance': usdt_balance
    }

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize Web3 connection to BSC
        print("Connecting to Binance Smart Chain...")
        web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        
        if not web3.is_connected():
            print("Error: Could not connect to BSC network")
            return
        
        print(f"Connected to BSC! Chain ID: {web3.eth.chain_id}")
        
        # Initialize token contracts
        usdc_contract = web3.eth.contract(
            address=Web3.to_checksum_address(USDC_BSC_CONTRACT),
            abi=ERC20_ABI
        )
        usdt_contract = web3.eth.contract(
            address=Web3.to_checksum_address(USDT_BSC_CONTRACT),
            abi=ERC20_ABI
        )
        
        print("\n" + "="*60)
        print("BSC BALANCE CHECKER")
        print("="*60)

        # Check special wallets
        special_total_bnb = 0.0
        special_total_usdc = 0.0
        special_total_usdt = 0.0
        if SPECIAL_WALLETS:
            print(f"\nSPECIAL WALLETS:")
            print("-" * 30)

            for i, address in enumerate(SPECIAL_WALLETS, 1):
                balance = check_single_wallet_balance(web3, usdc_contract, usdt_contract, address)

                print(f"\nSpecial Wallet {i}:")
                print(f"  Address: {balance['address']}")
                print(f"  BNB Balance: {balance['bnb_balance']:.6f} BNB")
                print(f"  USDC Balance: {balance['usdc_balance']:.6f} USDC")
                print(f"  USDT Balance: {balance['usdt_balance']:.6f} USDT")

                special_total_bnb += balance['bnb_balance']
                special_total_usdc += balance['usdc_balance']
                special_total_usdt += balance['usdt_balance']

        # Show summary for special wallets only
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)

        if SPECIAL_WALLETS:
            print(f"Special Wallets Checked: {len(SPECIAL_WALLETS)}")
            print(f"Special Wallets BNB Balance: {special_total_bnb:.6f} BNB")
            print(f"Special Wallets USDC Balance: {special_total_usdc:.6f} USDC")
            print(f"Special Wallets USDT Balance: {special_total_usdt:.6f} USDT")

        print(f"\nTOTAL:")
        print(f"Total BNB: {special_total_bnb:.6f} BNB")
        print(f"Total USDC: {special_total_usdc:.6f} USDC")
        print(f"Total USDT: {special_total_usdt:.6f} USDT")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
