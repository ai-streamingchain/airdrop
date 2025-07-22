#!/usr/bin/env python3
"""
Build script to create executable from BSC Balance Checker GUI
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    print("BSC Wallet Manager - Build Script")
    print("=" * 50)
    
    # Check if Python is available
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"Using Python: {python_version}")
    except Exception as e:
        print(f"Error checking Python version: {e}")
        return False
    
    # Install/upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}")
    
    # Remove .spec files
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"✓ Removed {spec_file}")
    
    # Build executable with PyInstaller using spec file
    pyinstaller_command = f"{sys.executable} -m PyInstaller BSC_Wallet_Manager.spec"
    
    if not run_command(pyinstaller_command, "Building executable with PyInstaller"):
        return False
    
    # Check if executable was created
    if os.name == 'nt':  # Windows
        exe_path = os.path.join("dist", "BSC_Wallet_Manager.exe")
    else:  # Linux/Mac
        exe_path = os.path.join("dist", "BSC_Wallet_Manager")
    
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
        print(f"\n✓ Build successful!")
        print(f"Executable created: {exe_path}")
        print(f"File size: {file_size:.1f} MB")
        
        # Create a simple README for the executable
        readme_content = """BSC Wallet Manager
==================

This is a comprehensive GUI application for BSC wallet management with two main features:

BALANCE CHECKER:
- Check BNB, USDC, and USDT balances on Binance Smart Chain
- Enter wallet addresses (one per line) and get real-time balances
- Shows individual wallet balances and totals

WALLET GENERATOR:
- Generate new BSC/Ethereum wallets
- Specify number of wallets to create (1-1000)
- View generated addresses and private keys
- Save wallets to CSV file for backup

How to use:
1. Run the BSC_Wallet_Manager executable
2. Use the tabs to switch between Balance Checker and Wallet Generator
3. Follow the instructions in each tab

SECURITY WARNING:
- Keep your private keys secure and never share them
- Back up your wallets safely
- This application connects to BSC mainnet for real data

Features:
- Dual-tab interface for easy navigation
- Real-time balance checking
- Secure wallet generation
- CSV export functionality
- Progress indicators
- Error handling and validation
"""
        
        with open(os.path.join("dist", "README.txt"), "w") as f:
            f.write(readme_content)
        
        print("✓ README.txt created in dist folder")
        
        return True
    else:
        print(f"\n✗ Build failed - executable not found at {exe_path}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 50)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("You can find the executable in the 'dist' folder.")
        print("The executable is standalone and doesn't require Python to be installed.")
    else:
        print("\n" + "=" * 50)
        print("BUILD FAILED!")
        print("=" * 50)
        print("Please check the error messages above and try again.")
    
    input("\nPress Enter to exit...")
