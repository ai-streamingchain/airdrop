### Airdrop Farming

## How to install envirtionment
- `Install python 3.11`
- `pip install -r requirements.txt`

## How to run
# Set .env file
- Number of wallets to create
`NUMBER_OF_WALLETS=10`

- Wallets file name to use
`WALLETS_FILE=wallets.csv`

- RPC URL of network
`WEB3_PROVIDER=HTTP://127.0.0.1:7545`

- Main wallet Information
`MAIN_WALLET_ADDRESS=0x556a09c6b6cF017Ec09916384b8E6EE8212d22b5`
`MAIN_WALLET_PRIVATE_KEY=0xb9ecba32a39d5f35d6ace5f265688423391c2d8869e29a83b1200ef33d50ed0b`

- The amount of native token to supply from main wallet
`TOKEN_AMOUNT=0.0001`

# Create wallets
- `python generate_wallets.py`
- `mv ./wallets/wallets_2025_6_14_13_15_16.csv wallets.csv`

# Supply the amount(TOKEN_AMOUNT) of native tokens to all wallets of wallets.csv file
- `python supply_native_token.py`
