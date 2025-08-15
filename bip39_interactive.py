#!/usr/bin/env python3
"""
Interactive BIP39 Offline Address Generator
Allows user to input their own mnemonic and generate addresses
"""

import sys
import os
from bip39_offline import BIP39, generate_addresses, export_to_csv

def get_user_input():
    """Get mnemonic and other parameters from user"""
    print("BIP39 Interactive Offline Address Generator")
    print("=" * 50)
    print()
    
    # Get mnemonic
    while True:
        mnemonic = input("Enter your BIP39 mnemonic phrase: ").strip()
        if not mnemonic:
            print("Please enter a valid mnemonic phrase.")
            continue
        
        # Validate mnemonic
        try:
            bip39 = BIP39()
            if bip39.validate_mnemonic(mnemonic):
                break
            else:
                print("Invalid mnemonic phrase. Please check your words and try again.")
        except Exception as e:
            print(f"Error validating mnemonic: {e}")
    
    # Get passphrase (optional)
    passphrase = input("Enter BIP39 passphrase (optional, press Enter to skip): ").strip()
    
    # Get number of addresses
    while True:
        try:
            num_addresses = input("Number of addresses to generate per derivation path (default: 10): ").strip()
            if not num_addresses:
                num_addresses = 10
            else:
                num_addresses = int(num_addresses)
            
            if num_addresses <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get output filename
    output_file = input("Output CSV filename (default: bip39_addresses.csv): ").strip()
    if not output_file:
        output_file = "bip39_addresses.csv"
    
    return mnemonic, passphrase, num_addresses, output_file

def display_seed_info(mnemonic, passphrase=""):
    """Display seed information"""
    bip39 = BIP39()
    seed = bip39.mnemonic_to_seed(mnemonic, passphrase)
    
    print(f"\nMnemonic: {mnemonic}")
    if passphrase:
        print(f"Passphrase: {passphrase}")
    print(f"BIP39 Seed: {seed.hex()}")
    print()

def main():
    """Main interactive function"""
    try:
        # Get user input
        mnemonic, passphrase, num_addresses, output_file = get_user_input()
        
        # Display seed info
        display_seed_info(mnemonic, passphrase)
        
        print("Generating addresses...")
        print()
        
        # Generate addresses
        results = generate_addresses(mnemonic, passphrase, num_addresses)
        
        # Display results
        for path_desc, addresses in results.items():
            print(f"{path_desc}")
            print("-" * len(path_desc))
            print(f"{'Index':<5} | {'Address':<42} | {'Script Semantics'}")
            print("-" * 70)
            
            for i, addr_info in enumerate(addresses):
                print(f"{i:<5} | {addr_info['address']:<42} | {addr_info['script_semantics']}")
            print()
        
        # Export to CSV
        export_to_csv(results, output_file)
        print(f"✓ Results exported to '{output_file}'")
        
        # Display summary
        print(f"\n" + "="*80)
        print("SUMMARY - First address of each derivation type:")
        print("="*80)
        
        summary_paths = [
            ("m/0'/0'/0'", "Legacy (Custom)"),
            ("m/44'/0'/0'/0/0", "BIP44 (Legacy P2PKH)"),
            ("m/49'/0'/0'/0/0", "BIP49 (P2WPKH nested in P2SH)"),
            ("m/84'/0'/0'/0/0", "BIP84 (Native SegWit P2WPKH)"),
            ("m/0/0", "Simple derivation")
        ]
        
        print(f"{'Path':<20} | {'Address':<42} | {'Script Semantics'}")
        print("-" * 85)
        
        for path, desc in summary_paths:
            # Find the corresponding result
            for path_desc, addresses in results.items():
                if len(addresses) > 0:
                    addr_info = addresses[0]
                    if path.replace('/0', '/0') in addr_info['path']:
                        print(f"{path:<20} | {addr_info['address']:<42} | {addr_info['script_semantics']}")
                        break
        
        print(f"\n✓ Generated {num_addresses} addresses for each of {len(results)} derivation paths")
        print(f"✓ Total addresses generated: {sum(len(addrs) for addrs in results.values())}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
