# PyInstaller hook for web3 package

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all data, binaries, and hidden imports for web3
datas, binaries, hiddenimports = collect_all('web3')

# Add additional hidden imports
hiddenimports += [
    'web3.auto',
    'web3.providers',
    'web3.providers.rpc',
    'web3.providers.ipc',
    'web3.providers.websocket',
    'web3.middleware',
    'web3.gas_strategies',
    'cytoolz',
    'toolz',
    'eth_abi',
    'eth_utils',
    'hexbytes',
    'requests',
]

# Collect all submodules
hiddenimports += collect_submodules('web3')
hiddenimports += collect_submodules('eth_account')
hiddenimports += collect_submodules('eth_keyfile')
