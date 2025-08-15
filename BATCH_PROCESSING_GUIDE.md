# BIP39 Batch Processing Guide

## 📋 **Overview**

The BIP39 offline tool now supports batch processing of multiple seeds from an input file. This feature is perfect for:

- Processing multiple mnemonic phrases at once
- Generating addresses for balance checking
- Bulk address generation for portfolio management

## 📁 **Files Added**

1. **`batch_process_seeds.py`** - Advanced batch processor with command-line options
2. **`process_seeds_simple.py`** - Simple batch processor with default settings
3. **`process_seeds.bat`** - Windows batch file for easy execution
4. **`seeds.txt`** - Input file containing mnemonic phrases (one per line)

## 🚀 **Quick Start**

### 1. Create Input File

Create a file named `seeds.txt` with one mnemonic phrase per line:

```
motor venture dilemma quote subject magnet keep large dry gossip bean paper
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
your other mnemonic phrase here
```

### 2. Run Processing

**Option A: Simple Mode (Recommended)**
```bash
python process_seeds_simple.py
```

**Option B: Windows Users**
```
Double-click process_seeds.bat
```

**Option C: Advanced Mode**
```bash
python batch_process_seeds.py -i seeds.txt -n 10
```

## 📊 **Output Files**

### 1. `bip39_addresses.csv` - Complete Data
Contains full information for each generated address:
- `seed_index` - Index of the seed in input file
- `seed` - Original mnemonic phrase
- `derivation_path` - BIP32 derivation path
- `address_index` - Index within derivation path
- `address` - Bitcoin address
- `public_key` - Public key (hex)
- `private_key` - Private key (hex)
- `private_key_wif` - Private key in WIF format
- `script_semantics` - Address type (P2PKH, P2WPKH, etc.)

### 2. `bip39_only_addresses.txt` - Addresses Only
Contains only Bitcoin addresses, one per line. Perfect for:
- Balance checking tools
- Address monitoring
- Import into other applications

Example:
```
1GyNWR7LPXdLSHeN4nE4b9P3gNEcjZkmzd
1GPruf7qZWTKbAmUH351MAwNpMVqJHjfUT
1Jo3qrSUxWYYJdhDawJ58QU7wtyVtqAK5A
bc1qnc9umhdc04u0u5qfg0qu3aj75wvfps4z4sj7g6
...
```

## ⚙️ **Advanced Options**

### Command Line Arguments

```bash
python batch_process_seeds.py [options]

Options:
  -i, --input FILE      Input file (default: seeds.txt)
  -c, --csv FILE        CSV output file (default: bip39_addresses.csv)
  -a, --addresses FILE  Addresses output file (default: bip39_only_addresses.txt)
  -n, --num NUMBER      Addresses per derivation path (default: 10)
```

### Examples

**Custom input file:**
```bash
python batch_process_seeds.py -i my_seeds.txt
```

**Generate 20 addresses per path:**
```bash
python batch_process_seeds.py -n 20
```

**Custom output files:**
```bash
python batch_process_seeds.py -c my_addresses.csv -a my_addresses_only.txt
```

## 📈 **Address Generation Details**

For each seed, the tool generates addresses from these derivation paths:

| Path Pattern | Description | Address Type | Count |
|-------------|-------------|--------------|-------|
| `m/0'/0'/X'` | BIP32 Custom | P2PKH | 10 |
| `m/44'/0'/0'/0/X'` | BIP44 Legacy | P2PKH | 10 |
| `m/49'/0'/0'/0/X'` | BIP49 SegWit | P2WPKH nested in P2SH | 10 |
| `m/84'/0'/0'/0/X'` | BIP84 Native SegWit | P2WPKH | 10 |
| `m/0/X'` | Simple derivation | P2SH + P2WPKH | 20 |

**Total: 60 addresses per seed** (with default settings)

## 🔒 **Security Notes**

- **Offline Processing**: All operations work offline
- **Input File Security**: Keep your `seeds.txt` file secure and delete after processing
- **Private Keys**: The CSV file contains private keys - handle with extreme care
- **Addresses File**: The addresses-only file is safe for balance checking

## 📋 **Sample Output**

```
BIP39 Seed Processor - Simple Mode
========================================
Reading from: seeds.txt
Output files:
  - bip39_addresses.csv (full data)
  - bip39_only_addresses.txt (addresses only)

Processing seeds from: seeds.txt
CSV output: bip39_addresses.csv
Addresses only output: bip39_only_addresses.txt
============================================================
Found 2 seed(s) to process

Processing seed 1/2: motor venture dilemma quote subject magnet keep la...
  ✓ Generated 60 addresses
Processing seed 2/2: abandon abandon abandon abandon abandon abandon ab...
  ✓ Generated 60 addresses

============================================================
✅ Processing completed!
📁 Full data saved to: bip39_addresses.csv
📋 Addresses only saved to: bip39_only_addresses.txt

✅ Processing complete!
📋 Use 'bip39_only_addresses.txt' for balance checking
```

## 🎯 **Use Cases**

### Balance Checking
Use `bip39_only_addresses.txt` with balance checking tools:
```bash
# Example with blockchain API tools
curl -X POST "https://api.example.com/check-balances" \
  --data-binary @bip39_only_addresses.txt
```

### Portfolio Management
Import addresses into portfolio tracking applications.

### Address Monitoring
Set up monitoring for all generated addresses.

## ⚠️ **Important Notes**

1. **Validation**: Only valid BIP39 mnemonic phrases are processed
2. **Error Handling**: Invalid seeds are skipped with warnings
3. **File Encoding**: All files use UTF-8 encoding
4. **Large Files**: Processing many seeds may take time
5. **Memory Usage**: Large batches may require significant memory

## 🔧 **Troubleshooting**

**File not found error:**
- Ensure `seeds.txt` exists in the same directory
- Check file permissions

**Invalid mnemonic warnings:**
- Verify mnemonic phrases are correct
- Check for extra spaces or characters

**Memory issues:**
- Process smaller batches
- Reduce number of addresses per path with `-n` option

The batch processing feature makes it easy to generate addresses for multiple seeds efficiently while maintaining the same security and accuracy as the single-seed processing!
