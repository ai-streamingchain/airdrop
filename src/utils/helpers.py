"""
Utility helper functions
"""

import re
from web3 import Web3

def is_valid_ethereum_address(address):
    """Check if a string is a valid Ethereum address"""
    if not address:
        return False
    
    # Check if it's a valid hex string with proper length
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    
    try:
        # Use Web3 to validate checksum
        return Web3.is_address(address)
    except:
        return False

def is_valid_private_key(private_key):
    """Check if a string is a valid private key"""
    if not private_key:
        return False
    
    # Remove 0x prefix if present
    if private_key.startswith('0x'):
        private_key = private_key[2:]
    
    # Check if it's a valid hex string with proper length (64 characters)
    if not re.match(r'^[a-fA-F0-9]{64}$', private_key):
        return False
    
    try:
        # Try to create an account from the private key
        Web3().eth.account.from_key('0x' + private_key)
        return True
    except:
        return False

def format_balance(balance, decimals=6):
    """Format balance with specified decimal places"""
    return f"{balance:.{decimals}f}"

def validate_positive_number(value_str, field_name="Value"):
    """Validate that a string represents a positive number"""
    try:
        value = float(value_str)
        if value <= 0:
            raise ValueError(f"{field_name} must be positive")
        return value
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"{field_name} must be a valid number")
        raise e

def validate_positive_integer(value_str, field_name="Value", max_value=None):
    """Validate that a string represents a positive integer"""
    try:
        value = int(value_str)
        if value <= 0:
            raise ValueError(f"{field_name} must be positive")
        if max_value and value > max_value:
            raise ValueError(f"{field_name} must not exceed {max_value}")
        return value
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"{field_name} must be a valid integer")
        raise e

def truncate_address(address, start_chars=6, end_chars=4):
    """Truncate an Ethereum address for display purposes"""
    if not address or len(address) < start_chars + end_chars:
        return address
    
    return f"{address[:start_chars]}...{address[-end_chars:]}"

def format_transaction_hash(tx_hash, start_chars=8, end_chars=6):
    """Format a transaction hash for display purposes"""
    if not tx_hash:
        return ""
    
    tx_str = tx_hash if isinstance(tx_hash, str) else tx_hash.hex()
    
    if len(tx_str) < start_chars + end_chars:
        return tx_str
    
    return f"{tx_str[:start_chars]}...{tx_str[-end_chars:]}"
