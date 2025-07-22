#!/usr/bin/env python3
"""
BSC Wallet Manager - Main Entry Point
=====================================

A comprehensive GUI application for BSC wallet management with three main features:
1. Balance Checker - Check BNB, USDC, and USDT balances
2. Wallet Generator - Generate new BSC/Ethereum wallets
3. Token Supplier - Supply native tokens to multiple wallets

Author: BSC Wallet Manager Team
Version: 1.0.0
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.wallet_manager_gui import BSCWalletManager
import tkinter as tk

def main():
    """Main entry point for the BSC Wallet Manager application"""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Initialize the application
        app = BSCWalletManager(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
