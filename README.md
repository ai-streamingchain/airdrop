# BSC Wallet Manager

A comprehensive GUI application for BSC wallet management with three main features:

## 🚀 Features

### 1. **Balance Checker**
- Check BNB, USDC, and USDT balances on Binance Smart Chain
- Support for multiple wallet addresses
- Real-time balance fetching from BSC mainnet
- Summary totals across all wallets

### 2. **Wallet Generator**
- Generate new BSC/Ethereum wallets (1-1000 wallets)
- Cryptographically secure wallet generation
- Export wallets to CSV with timestamps
- View addresses and private keys

### 3. **Token Supplier**
- Distribute native BNB tokens to multiple wallets
- CSV file support for bulk operations
- Transaction tracking and reporting
- Configuration validation

## 📁 Project Structure

```
airdrop/
├── main.py                 # Main entry point
├── build.py               # Build script for executable
├── build.bat             # Windows build script
├── requirements.txt      # Python dependencies
├── .env                 # Environment configuration
├── README.md           # This file
└── src/
    ├── gui/
    │   └── wallet_manager_gui.py    # Main GUI application
    ├── core/
    │   ├── blockchain.py            # BSC blockchain interactions
    │   ├── wallet_generator.py      # Wallet generation logic
    │   └── token_supplier.py        # Token distribution logic
    ├── utils/
    │   └── helpers.py              # Utility functions
    └── legacy/                     # Old script files
```

## 🛠️ Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎮 How to Run

### Method 1: Run GUI Application
```bash
python main.py
```

### Method 2: Build Standalone Executable
```bash
python build.py
# or on Windows:
build.bat
```

The executable will be created in the `dist/` folder.

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# Main wallet configuration (for token supplier)
MAIN_WALLET_ADDRESS=0x556a09c6b6cF017Ec09916384b8E6EE8212d22b5
MAIN_WALLET_PRIVATE_KEY=0xb9ecba32a39d5f35d6ace5f265688423391c2d8869e29a83b1200ef33d50ed0b

# Token distribution settings
TOKEN_AMOUNT=0.001
WALLETS_FILE=wallets.csv

# Optional: API keys for enhanced features
ETHERSCAN_API_KEY=your_api_key_here
```

## 🔒 Security Notes

- **Never share your private keys**
- **Keep your .env file secure and never commit it to version control**
- **Always verify addresses before sending transactions**
- **Test with small amounts first**

## 📖 Usage Guide

### Balance Checker Tab
1. Enter wallet addresses (one per line)
2. Click "Check Balances"
3. View individual and total balances

### Wallet Generator Tab
1. Enter number of wallets to generate
2. Click "Generate Wallets"
3. Save to CSV for backup

### Token Supplier Tab
1. Configure main wallet details
2. Select CSV file with recipient wallets
3. Set token amount per wallet
4. Validate configuration
5. Start token distribution

## 🏗️ Development

The project uses a modular structure:

- **GUI Layer**: `src/gui/` - User interface components
- **Core Logic**: `src/core/` - Business logic and blockchain interactions
- **Utilities**: `src/utils/` - Helper functions and validators
- **Legacy**: `src/legacy/` - Old script files for reference

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**: Check your internet connection and BSC RPC endpoint
2. **Invalid Address**: Ensure wallet addresses are valid Ethereum format
3. **Insufficient Balance**: Verify main wallet has enough BNB for distribution
4. **CSV Format**: Ensure CSV file has correct format (no, address, private_key)

### Getting Help

If you encounter issues:
1. Check the error messages in the application
2. Verify your configuration in `.env`
3. Ensure all dependencies are installed
4. Check network connectivity

## 📄 License

This project is for educational and personal use. Use at your own risk.
