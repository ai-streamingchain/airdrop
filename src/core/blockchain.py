"""
Blockchain interaction module for BSC operations
"""

from web3 import Web3
import json

# BSC Network Configuration
BSC_RPC_URL = "https://bsc-dataseed1.binance.org/"
BSC_CHAIN_ID = 56

# Token Contract Addresses on BSC
USDC_BSC_CONTRACT = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
USDT_BSC_CONTRACT = "0x55d398326f99059ff775485246999027b3197955"

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

class BSCBlockchain:
    """BSC blockchain interaction class"""
    
    def __init__(self):
        self.web3 = None
        self.usdc_contract = None
        self.usdt_contract = None
        self.connected = False
    
    def connect(self):
        """Connect to BSC network"""
        try:
            self.web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
            
            if not self.web3.is_connected():
                raise Exception("Could not connect to BSC network")
            
            # Initialize token contracts
            self.usdc_contract = self.web3.eth.contract(
                address=Web3.to_checksum_address(USDC_BSC_CONTRACT),
                abi=ERC20_ABI
            )
            self.usdt_contract = self.web3.eth.contract(
                address=Web3.to_checksum_address(USDT_BSC_CONTRACT),
                abi=ERC20_ABI
            )
            
            self.connected = True
            return True
            
        except Exception as e:
            self.connected = False
            raise Exception(f"Failed to connect to BSC: {str(e)}")
    
    def get_bnb_balance(self, address):
        """Get BNB balance for a given address"""
        if not self.connected:
            raise Exception("Not connected to BSC network")
        
        try:
            balance_wei = self.web3.eth.get_balance(address)
            balance_bnb = self.web3.from_wei(balance_wei, 'ether')
            return float(balance_bnb)
        except Exception as e:
            raise Exception(f"Error getting BNB balance for {address}: {str(e)}")
    
    def get_token_balance(self, address, token_contract, token_name):
        """Get token balance for a given address"""
        if not self.connected:
            raise Exception("Not connected to BSC network")
        
        try:
            balance_raw = token_contract.functions.balanceOf(address).call()
            decimals = token_contract.functions.decimals().call()
            balance_token = balance_raw / (10 ** decimals)
            return float(balance_token)
        except Exception as e:
            raise Exception(f"Error getting {token_name} balance for {address}: {str(e)}")
    
    def get_usdc_balance(self, address):
        """Get USDC balance for a given address"""
        return self.get_token_balance(address, self.usdc_contract, "USDC")
    
    def get_usdt_balance(self, address):
        """Get USDT balance for a given address"""
        return self.get_token_balance(address, self.usdt_contract, "USDT")
    
    def check_wallet_balance(self, address):
        """Check BNB, USDC, and USDT balance for a single wallet"""
        bnb_balance = self.get_bnb_balance(address)
        usdc_balance = self.get_usdc_balance(address)
        usdt_balance = self.get_usdt_balance(address)
        
        return {
            'address': address,
            'bnb_balance': bnb_balance,
            'usdc_balance': usdc_balance,
            'usdt_balance': usdt_balance
        }
    
    def transfer_native_token(self, from_wallet, to_address, amount_wei):
        """Transfer native tokens (BNB) from one wallet to another"""
        if not self.connected:
            raise Exception("Not connected to BSC network")
        
        try:
            # Get the nonce
            nonce = self.web3.eth.get_transaction_count(from_wallet.address)
            
            # Get the current gas price
            gas_price = self.web3.eth.gas_price
            
            # Build the transaction
            transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,  # Standard gas limit for BNB transfers
                'gasPrice': gas_price,
                'chainId': self.web3.eth.chain_id
            }
            
            # Sign the transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, from_wallet.key)
            
            # Send the transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            return receipt
            
        except Exception as e:
            raise Exception(f"Error in transfer: {str(e)}")
    
    def get_chain_id(self):
        """Get the current chain ID"""
        if not self.connected:
            return None
        return self.web3.eth.chain_id
