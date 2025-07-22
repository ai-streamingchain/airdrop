#!/usr/bin/env python3
"""
Simple build script that creates a more reliable executable
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
    print("BSC Wallet Manager - Simple Build Script")
    print("=" * 50)
    
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
    
    # Create a simple batch file for Windows
    if os.name == 'nt':  # Windows
        batch_content = f'''@echo off
cd /d "%~dp0"
"{sys.executable}" main.py
pause
'''
        with open("BSC_Wallet_Manager.bat", "w") as f:
            f.write(batch_content)
        print("✓ Created BSC_Wallet_Manager.bat")
    
    # Create a shell script for Linux/Mac
    else:
        shell_content = f'''#!/bin/bash
cd "$(dirname "$0")"
{sys.executable} main.py
read -p "Press Enter to exit..."
'''
        with open("BSC_Wallet_Manager.sh", "w") as f:
            f.write(shell_content)
        os.chmod("BSC_Wallet_Manager.sh", 0o755)
        print("✓ Created BSC_Wallet_Manager.sh")
    
    # Try PyInstaller build with simpler approach
    print("\nAttempting PyInstaller build...")
    
    simple_command = (
        f"{sys.executable} -m PyInstaller "
        "--onefile "
        "--windowed "
        "--name BSC_Wallet_Manager_Simple "
        "--add-data src;src "
        "--hidden-import tkinter "
        "--hidden-import tkinter.ttk "
        "--hidden-import tkinter.scrolledtext "
        "--hidden-import tkinter.messagebox "
        "--hidden-import tkinter.filedialog "
        "run_simple.py"
    )
    
    if run_command(simple_command, "Building with PyInstaller (simple approach)"):
        print("✓ PyInstaller build successful!")
        
        # Check if executable was created
        if os.name == 'nt':  # Windows
            exe_path = os.path.join("dist", "BSC_Wallet_Manager_Simple.exe")
        else:  # Linux/Mac
            exe_path = os.path.join("dist", "BSC_Wallet_Manager_Simple")
        
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"Executable created: {exe_path}")
            print(f"File size: {file_size:.1f} MB")
        
    else:
        print("✗ PyInstaller build failed, but batch/shell script is available")
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETED!")
    print("=" * 50)
    print("You can run the application using:")
    if os.name == 'nt':
        print("1. Double-click BSC_Wallet_Manager.bat")
        print("2. Or run: python main.py")
        if os.path.exists("dist/BSC_Wallet_Manager_Simple.exe"):
            print("3. Or use the executable: dist/BSC_Wallet_Manager_Simple.exe")
    else:
        print("1. Run: ./BSC_Wallet_Manager.sh")
        print("2. Or run: python main.py")
        if os.path.exists("dist/BSC_Wallet_Manager_Simple"):
            print("3. Or use the executable: dist/BSC_Wallet_Manager_Simple")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
