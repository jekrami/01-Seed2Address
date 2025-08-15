#!/usr/bin/env python3
"""
Batch process multiple seeds from input file and generate addresses
Reads seeds from input file and generates all addresses for balance checking
"""

import sys
import argparse
from bip39_offline import process_seeds_file

def main():
    """Main function for batch processing seeds"""
    
    parser = argparse.ArgumentParser(description='Batch process BIP39 seeds and generate addresses')
    parser.add_argument('-i', '--input', default='seeds.txt', 
                       help='Input file containing seeds (default: seeds.txt)')
    parser.add_argument('-c', '--csv', default='bip39_addresses.csv',
                       help='CSV output file with full data (default: bip39_addresses.csv)')
    parser.add_argument('-a', '--addresses', default='bip39_only_addresses.txt',
                       help='Text output file with addresses only (default: bip39_only_addresses.txt)')
    parser.add_argument('-n', '--num', type=int, default=10,
                       help='Number of addresses per derivation path (default: 10)')
    
    args = parser.parse_args()
    
    print("BIP39 Batch Seed Processor")
    print("=" * 50)
    print(f"Input file: {args.input}")
    print(f"CSV output: {args.csv}")
    print(f"Addresses output: {args.addresses}")
    print(f"Addresses per path: {args.num}")
    print()
    
    # Process the seeds
    process_seeds_file(
        input_file=args.input,
        csv_output=args.csv,
        addresses_output=args.addresses,
        num_addresses=args.num
    )

if __name__ == "__main__":
    main()
