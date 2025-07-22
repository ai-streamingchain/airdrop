"""
BSC Wallet Manager GUI - Main interface with three tabs:
1. Balance Checker
2. Wallet Generator  
3. Token Supplier
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from dotenv import load_dotenv

try:
    # Try relative imports first (for PyInstaller)
    from ..core.blockchain import BSCBlockchain
    from ..core.wallet_generator import WalletGenerator
    from ..core.token_supplier import TokenSupplier
    from ..utils.helpers import (
        is_valid_ethereum_address,
        is_valid_private_key,
        validate_positive_number,
        validate_positive_integer,
        format_balance
    )
except ImportError:
    # Fall back to absolute imports (for direct execution)
    from core.blockchain import BSCBlockchain
    from core.wallet_generator import WalletGenerator
    from core.token_supplier import TokenSupplier
    from utils.helpers import (
        is_valid_ethereum_address,
        is_valid_private_key,
        validate_positive_number,
        validate_positive_integer,
        format_balance
    )

# Default special wallets
DEFAULT_SPECIAL_WALLETS = [
    "0xBFe3A307dbADBd4dF9146EE5E694A268C4758141",
    "0xF791479FBDb9d385DCA288229Bd7269Ca7325432"
]

class BSCWalletManager:
    """Main BSC Wallet Manager GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BSC Wallet Manager v1.0")
        self.root.geometry("1000x800")
        
        # Initialize core components
        self.blockchain = BSCBlockchain()
        self.wallet_generator = WalletGenerator()
        self.token_supplier = TokenSupplier()
        
        # Load environment variables
        load_dotenv()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.setup_balance_checker_tab()
        self.setup_wallet_generator_tab()
        self.setup_token_supplier_tab()
        
    def setup_balance_checker_tab(self):
        """Setup the Balance Checker tab"""
        # Balance Checker Tab
        self.balance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.balance_frame, text="Balance Checker")
        
        # Configure grid weights
        self.balance_frame.columnconfigure(1, weight=1)
        self.balance_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(self.balance_frame, text="BSC Balance Checker", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Wallet addresses input
        ttk.Label(self.balance_frame, text="Wallet Addresses (one per line):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        self.wallet_text = scrolledtext.ScrolledText(self.balance_frame, height=8, width=70)
        self.wallet_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        # Pre-fill with default wallets
        default_wallets = "\n".join(DEFAULT_SPECIAL_WALLETS)
        self.wallet_text.insert("1.0", default_wallets)
        
        # Buttons frame
        balance_button_frame = ttk.Frame(self.balance_frame)
        balance_button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        self.check_button = ttk.Button(balance_button_frame, text="Check Balances", command=self.start_balance_check)
        self.check_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_balance_button = ttk.Button(balance_button_frame, text="Clear Results", command=self.clear_balance_results)
        self.clear_balance_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.balance_progress = ttk.Progressbar(self.balance_frame, mode='indeterminate')
        self.balance_progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        # Results area
        ttk.Label(self.balance_frame, text="Results:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        self.balance_results_text = scrolledtext.ScrolledText(self.balance_frame, height=15, width=80, font=("Consolas", 10))
        self.balance_results_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        
    def setup_wallet_generator_tab(self):
        """Setup the Wallet Generator tab"""
        # Wallet Generator Tab
        self.generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_frame, text="Wallet Generator")
        
        # Configure grid weights
        self.generator_frame.columnconfigure(1, weight=1)
        self.generator_frame.rowconfigure(5, weight=1)
        
        # Title
        title_label = ttk.Label(self.generator_frame, text="Wallet Generator", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Number of wallets input
        input_frame = ttk.Frame(self.generator_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        ttk.Label(input_frame, text="Number of wallets to generate:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.num_wallets_var = tk.StringVar(value="10")
        self.num_wallets_entry = ttk.Entry(input_frame, textvariable=self.num_wallets_var, width=10)
        self.num_wallets_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Generator buttons
        gen_button_frame = ttk.Frame(self.generator_frame)
        gen_button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        self.generate_button = ttk.Button(gen_button_frame, text="Generate Wallets", command=self.start_wallet_generation)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(gen_button_frame, text="Save to CSV", command=self.save_wallets_to_csv)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_gen_button = ttk.Button(gen_button_frame, text="Clear", command=self.clear_generated_wallets)
        self.clear_gen_button.pack(side=tk.LEFT)
        
        # Progress bar for generation
        self.gen_progress = ttk.Progressbar(self.generator_frame, mode='indeterminate')
        self.gen_progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        # Generated wallets display
        ttk.Label(self.generator_frame, text="Generated Wallets:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        self.generated_text = scrolledtext.ScrolledText(self.generator_frame, height=20, width=80, font=("Consolas", 9))
        self.generated_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        
    def setup_token_supplier_tab(self):
        """Setup the Token Supplier tab"""
        # Token Supplier Tab
        self.supplier_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.supplier_frame, text="Token Supplier")
        
        # Configure grid weights
        self.supplier_frame.columnconfigure(1, weight=1)
        self.supplier_frame.rowconfigure(7, weight=1)
        
        # Title
        title_label = ttk.Label(self.supplier_frame, text="Native Token Supplier", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Main wallet configuration
        config_frame = ttk.LabelFrame(self.supplier_frame, text="Main Wallet Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Main wallet address
        ttk.Label(config_frame, text="Main Wallet Address:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.main_address_var = tk.StringVar(value=os.getenv('MAIN_WALLET_ADDRESS', ''))
        self.main_address_entry = ttk.Entry(config_frame, textvariable=self.main_address_var, width=50)
        self.main_address_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Main wallet private key
        ttk.Label(config_frame, text="Main Wallet Private Key:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.main_key_var = tk.StringVar(value=os.getenv('MAIN_WALLET_PRIVATE_KEY', ''))
        self.main_key_entry = ttk.Entry(config_frame, textvariable=self.main_key_var, width=50, show="*")
        self.main_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Token amount
        ttk.Label(config_frame, text="Token Amount (BNB):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.token_amount_var = tk.StringVar(value=os.getenv('TOKEN_AMOUNT', '0.001'))
        self.token_amount_entry = ttk.Entry(config_frame, textvariable=self.token_amount_var, width=20)
        self.token_amount_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # CSV file selection
        file_frame = ttk.Frame(self.supplier_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Wallets CSV File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.csv_file_var = tk.StringVar(value=os.getenv('WALLETS_FILE', 'wallets.csv'))
        self.csv_file_entry = ttk.Entry(file_frame, textvariable=self.csv_file_var, width=40)
        self.csv_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        
        self.browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_csv_file)
        self.browse_button.grid(row=0, column=2, pady=(0, 5))
        
        # Supply buttons
        supply_button_frame = ttk.Frame(self.supplier_frame)
        supply_button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        self.validate_button = ttk.Button(supply_button_frame, text="Validate Configuration", command=self.validate_supplier_config)
        self.validate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.supply_button = ttk.Button(supply_button_frame, text="Start Token Supply", command=self.start_token_supply)
        self.supply_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_supply_button = ttk.Button(supply_button_frame, text="Clear Results", command=self.clear_supply_results)
        self.clear_supply_button.pack(side=tk.LEFT)
        
        # Progress bar for supply
        self.supply_progress = ttk.Progressbar(self.supplier_frame, mode='indeterminate')
        self.supply_progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))
        
        # Supply results display
        ttk.Label(self.supplier_frame, text="Supply Results:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        self.supply_results_text = scrolledtext.ScrolledText(self.supplier_frame, height=15, width=80, font=("Consolas", 10))
        self.supply_results_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))

    # Balance Checker Methods
    def log_balance_message(self, message):
        """Add message to balance results area"""
        self.balance_results_text.insert(tk.END, message + "\n")
        self.balance_results_text.see(tk.END)
        self.root.update_idletasks()

    def clear_balance_results(self):
        """Clear the balance results area"""
        self.balance_results_text.delete("1.0", tk.END)

    def start_balance_check(self):
        """Start balance checking in a separate thread"""
        # Disable button during check
        self.check_button.config(state='disabled')
        self.balance_progress.start()

        # Start checking in background thread
        thread = threading.Thread(target=self.check_balances)
        thread.daemon = True
        thread.start()

    def check_balances(self):
        """Main balance checking logic"""
        try:
            self.log_balance_message("Connecting to Binance Smart Chain...")

            # Connect to blockchain
            self.blockchain.connect()
            self.log_balance_message(f"Connected to BSC! Chain ID: {self.blockchain.get_chain_id()}")

            # Get wallet addresses from text input
            wallet_text = self.wallet_text.get("1.0", tk.END).strip()
            wallet_addresses = [addr.strip() for addr in wallet_text.split('\n') if addr.strip()]

            if not wallet_addresses:
                self.log_balance_message("No wallet addresses provided!")
                return

            # Validate addresses
            valid_addresses = []
            for addr in wallet_addresses:
                if is_valid_ethereum_address(addr):
                    valid_addresses.append(addr)
                else:
                    self.log_balance_message(f"Invalid address skipped: {addr}")

            if not valid_addresses:
                self.log_balance_message("No valid wallet addresses found!")
                return

            self.log_balance_message("\n" + "="*60)
            self.log_balance_message("BSC BALANCE CHECKER")
            self.log_balance_message("="*60)

            # Check each wallet
            total_bnb = 0.0
            total_usdc = 0.0
            total_usdt = 0.0

            for i, address in enumerate(valid_addresses, 1):
                try:
                    self.log_balance_message(f"\nWallet {i}:")
                    balance = self.blockchain.check_wallet_balance(address)

                    self.log_balance_message(f"  Address: {balance['address']}")
                    self.log_balance_message(f"  BNB Balance: {format_balance(balance['bnb_balance'])} BNB")
                    self.log_balance_message(f"  USDC Balance: {format_balance(balance['usdc_balance'])} USDC")
                    self.log_balance_message(f"  USDT Balance: {format_balance(balance['usdt_balance'])} USDT")

                    total_bnb += balance['bnb_balance']
                    total_usdc += balance['usdc_balance']
                    total_usdt += balance['usdt_balance']

                except Exception as e:
                    self.log_balance_message(f"  Error checking wallet {address}: {str(e)}")

            # Show summary
            self.log_balance_message("\n" + "="*60)
            self.log_balance_message("SUMMARY")
            self.log_balance_message("="*60)
            self.log_balance_message(f"Wallets Checked: {len(valid_addresses)}")
            self.log_balance_message(f"Total BNB: {format_balance(total_bnb)} BNB")
            self.log_balance_message(f"Total USDC: {format_balance(total_usdc)} USDC")
            self.log_balance_message(f"Total USDT: {format_balance(total_usdt)} USDT")

            self.log_balance_message("\nBalance check completed!")

        except Exception as e:
            self.log_balance_message(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Re-enable button and stop progress
            self.check_button.config(state='normal')
            self.balance_progress.stop()

    # Wallet Generator Methods
    def log_generated_wallet(self, message):
        """Add message to generated wallets area"""
        self.generated_text.insert(tk.END, message + "\n")
        self.generated_text.see(tk.END)
        self.root.update_idletasks()

    def clear_generated_wallets(self):
        """Clear the generated wallets area"""
        self.generated_text.delete("1.0", tk.END)
        self.wallet_generator.clear_generated_wallets()

    def start_wallet_generation(self):
        """Start wallet generation in a separate thread"""
        try:
            num_wallets = validate_positive_integer(self.num_wallets_var.get(), "Number of wallets", 1000)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Disable button during generation
        self.generate_button.config(state='disabled')
        self.gen_progress.start()

        # Start generation in background thread
        thread = threading.Thread(target=self.generate_wallets_thread, args=(num_wallets,))
        thread.daemon = True
        thread.start()

    def generate_wallets_thread(self, num_wallets):
        """Wallet generation thread"""
        try:
            self.log_generated_wallet(f"Generating {num_wallets} wallets...")
            self.log_generated_wallet("=" * 50)

            # Generate wallets with progress callback
            wallets = self.wallet_generator.generate_wallets(num_wallets, self.log_generated_wallet)

            self.log_generated_wallet("=" * 50)
            self.log_generated_wallet(f"Successfully generated {len(wallets)} wallets!")
            self.log_generated_wallet("\nWallet Details:")
            self.log_generated_wallet("-" * 30)

            for wallet in wallets:
                self.log_generated_wallet(f"No: {wallet['no']}")
                self.log_generated_wallet(f"Address: {wallet['address']}")
                self.log_generated_wallet(f"Private Key: {wallet['private_key']}")
                self.log_generated_wallet("-" * 30)

            self.log_generated_wallet("\nIMPORTANT: Keep your private keys secure and never share them!")

        except Exception as e:
            self.log_generated_wallet(f"Error generating wallets: {str(e)}")
            messagebox.showerror("Error", f"Error generating wallets: {str(e)}")

        finally:
            # Re-enable button and stop progress
            self.generate_button.config(state='normal')
            self.gen_progress.stop()

    def save_wallets_to_csv(self):
        """Save generated wallets to CSV file"""
        wallets = self.wallet_generator.get_generated_wallets()
        if not wallets:
            messagebox.showwarning("Warning", "No wallets generated yet!")
            return

        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialname="generated_wallets.csv"
        )

        if filename:
            try:
                filepath = self.wallet_generator.save_wallets_to_csv(os.path.basename(filename))
                messagebox.showinfo("Success", f"Wallets saved to {filepath}")
                self.log_generated_wallet(f"\nWallets saved to: {filepath}")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    # Token Supplier Methods
    def log_supply_message(self, message):
        """Add message to supply results area"""
        self.supply_results_text.insert(tk.END, message + "\n")
        self.supply_results_text.see(tk.END)
        self.root.update_idletasks()

    def clear_supply_results(self):
        """Clear the supply results area"""
        self.supply_results_text.delete("1.0", tk.END)

    def browse_csv_file(self):
        """Browse for CSV file"""
        filename = filedialog.askopenfilename(
            title="Select Wallets CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file_var.set(filename)

    def validate_supplier_config(self):
        """Validate the token supplier configuration"""
        try:
            # Validate main wallet address
            main_address = self.main_address_var.get().strip()
            if not main_address:
                raise ValueError("Main wallet address is required")
            if not is_valid_ethereum_address(main_address):
                raise ValueError("Invalid main wallet address")

            # Validate private key
            main_key = self.main_key_var.get().strip()
            if not main_key:
                raise ValueError("Main wallet private key is required")
            if not is_valid_private_key(main_key):
                raise ValueError("Invalid private key format")

            # Validate token amount
            token_amount = validate_positive_number(self.token_amount_var.get(), "Token amount")

            # Validate CSV file
            csv_file = self.csv_file_var.get().strip()
            if not csv_file:
                raise ValueError("CSV file path is required")
            if not os.path.exists(csv_file):
                raise ValueError("CSV file does not exist")

            # Connect to network and validate wallet
            self.log_supply_message("Validating configuration...")
            self.token_supplier.connect_to_network()

            # Check if address matches private key
            if not self.token_supplier.validate_main_wallet(main_address, main_key):
                raise ValueError("Main wallet address does not match private key")

            # Check main wallet balance
            balance = self.token_supplier.get_main_wallet_balance(main_address)
            self.log_supply_message(f"Main wallet balance: {format_balance(balance)} BNB")

            # Read and validate CSV file
            wallets = self.token_supplier.read_wallets_from_csv(csv_file)
            self.log_supply_message(f"Found {len(wallets)} wallets in CSV file")

            # Calculate total amount needed
            total_needed = len(wallets) * token_amount
            self.log_supply_message(f"Total amount needed: {format_balance(total_needed)} BNB")

            if balance < total_needed:
                self.log_supply_message("WARNING: Insufficient balance for all transfers!")
            else:
                self.log_supply_message("✓ Configuration is valid and ready for token supply")

            messagebox.showinfo("Validation", "Configuration validated successfully!")

        except Exception as e:
            self.log_supply_message(f"Validation error: {str(e)}")
            messagebox.showerror("Validation Error", str(e))

    def start_token_supply(self):
        """Start token supply in a separate thread"""
        try:
            # Validate inputs
            main_address = self.main_address_var.get().strip()
            main_key = self.main_key_var.get().strip()
            token_amount = validate_positive_number(self.token_amount_var.get(), "Token amount")
            csv_file = self.csv_file_var.get().strip()

            if not all([main_address, main_key, csv_file]):
                raise ValueError("All fields are required")

            # Confirm with user
            if not messagebox.askyesno("Confirm", "Are you sure you want to start token distribution? This will send real transactions."):
                return

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Disable button during supply
        self.supply_button.config(state='disabled')
        self.supply_progress.start()

        # Start supply in background thread
        thread = threading.Thread(target=self.supply_tokens_thread, args=(main_key, token_amount, csv_file))
        thread.daemon = True
        thread.start()

    def supply_tokens_thread(self, main_key, token_amount, csv_file):
        """Token supply thread"""
        try:
            self.log_supply_message("Starting token distribution...")
            self.log_supply_message("=" * 60)

            # Connect to network
            self.token_supplier.connect_to_network()

            # Read wallets from CSV
            wallets = self.token_supplier.read_wallets_from_csv(csv_file)
            self.log_supply_message(f"Loaded {len(wallets)} wallets from CSV")

            # Start distribution
            summary = self.token_supplier.supply_tokens_to_wallets(
                main_key, wallets, token_amount, self.log_supply_message
            )

            # Show final summary
            self.log_supply_message("\n" + "="*60)
            self.log_supply_message("DISTRIBUTION SUMMARY")
            self.log_supply_message("="*60)
            self.log_supply_message(f"Total wallets: {summary['total_wallets']}")
            self.log_supply_message(f"Successful transfers: {summary['successful_transfers']}")
            self.log_supply_message(f"Failed transfers: {summary['failed_transfers']}")
            self.log_supply_message(f"Total amount distributed: {format_balance(summary['total_amount_distributed'])} BNB")

            if summary['failed_transfers'] > 0:
                self.log_supply_message("\nFailed transfers:")
                for result in summary['results']:
                    if result['status'] == 'failed':
                        self.log_supply_message(f"  {result['address']}: {result.get('error', 'Unknown error')}")

            self.log_supply_message("\nToken distribution completed!")

        except Exception as e:
            self.log_supply_message(f"Error during token distribution: {str(e)}")
            messagebox.showerror("Error", f"Error during token distribution: {str(e)}")

        finally:
            # Re-enable button and stop progress
            self.supply_button.config(state='normal')
            self.supply_progress.stop()
