#!/usr/bin/env python3
"""
Simple script to process seeds from seeds.txt file
Generates addresses for balance checking
"""

from bip39_offline import process_seeds_file

def main():
    """Simple main function to process seeds with default settings"""
    
    print("BIP39 Seed Processor - Simple Mode")
    print("=" * 40)
    print("Reading from: seeds.txt")
    print("Output files:")
    print("  - bip39_addresses.csv (full data)")
    print("  - bip39_only_addresses.txt (addresses only)")
    print()
    
    # Process with default settings
    process_seeds_file(
        input_file="seeds.txt",
        csv_output="bip39_addresses.csv", 
        addresses_output="bip39_only_addresses.txt",
        num_addresses=10
    )
    
    print()
    print("✅ Processing complete!")
    print("📋 Use 'bip39_only_addresses.txt' for balance checking")

if __name__ == "__main__":
    main()
