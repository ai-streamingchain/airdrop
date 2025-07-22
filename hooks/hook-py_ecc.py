# PyInstaller hook for py_ecc package

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all data, binaries, and hidden imports for py_ecc
datas, binaries, hiddenimports = collect_all('py_ecc')

# Add additional hidden imports that might be missed
hiddenimports += [
    'py_ecc.bn128',
    'py_ecc.secp256k1',
    'py_ecc.bls',
    'py_ecc.optimized_bn128',
]

# Collect all submodules
hiddenimports += collect_submodules('py_ecc')
