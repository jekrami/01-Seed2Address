@echo off
echo BIP39 Seed Processor
echo ===================
echo.
echo This script will:
echo 1. Read seeds from 'seeds.txt' file
echo 2. Generate all addresses for each seed
echo 3. Create 'bip39_addresses.csv' with full data
echo 4. Create 'bip39_only_addresses.txt' for balance checking
echo.
if not exist seeds.txt (
    echo ERROR: seeds.txt file not found!
    echo Please create seeds.txt with one mnemonic phrase per line.
    echo.
    pause
    exit /b 1
)
echo Processing seeds...
python process_seeds_simple.py
echo.
echo Files created:
if exist bip39_addresses.csv echo   ✓ bip39_addresses.csv
if exist bip39_only_addresses.txt echo   ✓ bip39_only_addresses.txt
echo.
pause
