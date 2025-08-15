# BIP39 Offline Address Generator

A Python-based offline tool for generating Bitcoin addresses from BIP39 mnemonic phrases. This tool provides the same functionality as the HTML-based BIP39 tool but works completely offline and can be used programmatically.

## Features

- ✅ **Offline Operation**: Works completely offline for maximum security
- ✅ **BIP39 Mnemonic Validation**: Validates mnemonic phrases with checksum verification
- ✅ **Multiple Derivation Paths**: Supports BIP32, BIP44, BIP49, BIP84 derivation standards
- ✅ **Multiple Address Types**: Generates Legacy (P2PKH), SegWit (P2WPKH), and P2SH addresses
- ✅ **CSV Export**: Exports results to CSV for easy analysis
- ✅ **Interactive Mode**: User-friendly interactive interface
- ✅ **Programmatic API**: Use as a Python library in your own projects

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Required Files**:
   - `bip39-english.csv` - BIP39 English wordlist (included)
   - `bip39_offline.py` - Main library
   - `bip39_interactive.py` - Interactive interface
   - `example_usage.py` - Usage examples

## Quick Start

### Test with Sample Data

Run the main script with the test mnemonic:

```bash
python bip39_offline.py
```

This will generate addresses for the test mnemonic: `"motor venture dilemma quote subject magnet keep large dry gossip bean paper"`

### Interactive Mode

For your own mnemonic phrase:

```bash
python bip39_interactive.py
```

This will prompt you to enter:
- Your BIP39 mnemonic phrase
- Optional passphrase
- Number of addresses to generate
- Output filename

### Programmatic Usage

```python
from bip39_offline import generate_addresses, BIP39

# Your mnemonic phrase
mnemonic = "your twelve word mnemonic phrase here"

# Generate 10 addresses for each derivation path
results = generate_addresses(mnemonic, num_addresses=10)

# Access specific addresses
bip44_addresses = results["m/44'/0'/0'/0 (BIP44 (Legacy))"]
first_address = bip44_addresses[0]["address"]
```

## Supported Derivation Paths

| Path | Description | Address Type | Script Semantics |
|------|-------------|--------------|-------------------|
| `m/0'/0'/0'` | Legacy Custom | P2PKH | Legacy addresses starting with '1' |
| `m/44'/0'/0'/0` | BIP44 Standard | P2PKH | Legacy addresses starting with '1' |
| `m/49'/0'/0'/0` | BIP49 SegWit | P2WPKH-P2SH | SegWit wrapped in P2SH starting with '3' |
| `m/84'/0'/0'/0` | BIP84 Native SegWit | P2WPKH | Native SegWit starting with 'bc1' |
| `m/0` | Simple derivation | P2PKH | Legacy addresses starting with '1' |

## Output Format

### Console Output
The tool displays addresses in a formatted table showing:
- Index (0-9 by default)
- Bitcoin Address
- Public Key (truncated)
- Private Key (truncated)
- Script Semantics

### CSV Export
Results are automatically exported to CSV with columns:
- `derivation_path`: Full BIP32 path
- `index`: Address index
- `address`: Bitcoin address
- `public_key`: Full public key (hex)
- `private_key`: Full private key (hex)
- `script_semantics`: Address type

## Security Considerations

⚠️ **IMPORTANT SECURITY NOTES**:

1. **Offline Use**: This tool is designed for offline use. Disconnect from the internet when handling real mnemonic phrases.

2. **Private Key Security**: The tool displays and exports private keys. Never share these with anyone.

3. **Mnemonic Security**: Your mnemonic phrase can recover all your funds. Keep it secure and private.

4. **Test First**: Always test with small amounts before using generated addresses for large transactions.

5. **Verify Addresses**: Cross-check generated addresses with other trusted tools when possible.

## Example Output

```
BIP39 Offline Address Generator
==================================================
Mnemonic: motor venture dilemma quote subject magnet keep large dry gossip bean paper

Generated Seed: 24bd1b243ec776dd97bc7487ad65c8966ff6e0b8654a25602a41994746957c49c...
Seed Match: True

m/44'/0'/0'/0 (BIP44 (Legacy))
------------------------------
Index | Address                                    | Script Semantics
0     | 1LDXHEixXvhQyVRHCN1fSHYCQUbHbPsPsq         | P2PKH
1     | 12EUk79AstuehDsjAHpnvcJdTB35xvpqHB         | P2PKH
...

m/84'/0'/0'/0 (BIP84 (Native SegWit))
-------------------------------------
Index | Address                                    | Script Semantics
0     | bc1qfnzvskgpv97fm7ewrmfgsymdf3wr47w4pguwua | P2WPKH
1     | bc1qusp7e0msy95ys9p3mhxy4v4v6aj8py9fpvjatj | P2WPKH
...
```

## Files Description

- **`bip39_offline.py`**: Main library with all BIP39/BIP32 functionality
- **`bip39_interactive.py`**: Interactive command-line interface
- **`example_usage.py`**: Examples showing how to use the library
- **`requirements.txt`**: Python dependencies
- **`bip39-english.csv`**: BIP39 English wordlist (2048 words)

## Validation

The tool has been tested against the reference implementation and produces identical results to the original HTML-based BIP39 tool for:
- Seed generation from mnemonic
- BIP32 key derivation
- Address generation for all supported types

## License

This tool is provided as-is for educational and personal use. Use at your own risk.

## Support

For issues or questions, please refer to the example files and ensure you understand Bitcoin address generation before using with real funds.
