#!/usr/bin/env python3
"""
Simple runner for BSC Wallet Manager without PyInstaller
This is useful for testing and development
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    import tkinter as tk
    from gui.wallet_manager_gui import BSCWalletManager
    
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
            import traceback
            traceback.print_exc()
            input("Press Enter to exit...")
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    input("Press Enter to exit...")
    sys.exit(1)
