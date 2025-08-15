#!/usr/bin/env python3
"""
Example usage of the BIP39 offline address generator
Shows how to use the library programmatically
"""

from bip39_offline import BIP39, generate_addresses, export_to_csv

def example_1():
    """Example 1: Basic usage with the test mnemonic"""
    print("Example 1: Basic Usage")
    print("=" * 30)
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Generate 5 addresses for each derivation path
    results = generate_addresses(mnemonic, num_addresses=5)
    
    # Display first address of each type
    for path_desc, addresses in results.items():
        first_addr = addresses[0]
        print(f"{path_desc}")
        print(f"  First address: {first_addr['address']}")
        print(f"  Script type: {first_addr['script_semantics']}")
        print()

def example_2():
    """Example 2: Using with passphrase"""
    print("Example 2: With Passphrase")
    print("=" * 30)
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    passphrase = "my_secret_passphrase"
    
    # Generate seed with passphrase
    bip39 = BIP39()
    seed_without_passphrase = bip39.mnemonic_to_seed(mnemonic)
    seed_with_passphrase = bip39.mnemonic_to_seed(mnemonic, passphrase)
    
    print(f"Seed without passphrase: {seed_without_passphrase.hex()[:32]}...")
    print(f"Seed with passphrase:    {seed_with_passphrase.hex()[:32]}...")
    print("Notice how the seeds are different!")
    print()

def example_3():
    """Example 3: Validate different mnemonics"""
    print("Example 3: Mnemonic Validation")
    print("=" * 30)
    
    bip39 = BIP39()
    
    test_mnemonics = [
        "motor venture dilemma quote subject magnet keep large dry gossip bean paper",  # Valid
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",  # Valid
        "invalid mnemonic phrase that should not work",  # Invalid
        "motor venture dilemma quote subject magnet keep large dry gossip bean",  # Invalid (wrong length)
    ]
    
    for mnemonic in test_mnemonics:
        is_valid = bip39.validate_mnemonic(mnemonic)
        print(f"'{mnemonic[:50]}...' -> {'Valid' if is_valid else 'Invalid'}")
    print()

def example_4():
    """Example 4: Generate specific derivation paths"""
    print("Example 4: Custom Derivation Paths")
    print("=" * 30)
    
    from bip39_offline import BIP32, BitcoinAddress
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    bip39 = BIP39()
    seed = bip39.mnemonic_to_seed(mnemonic)
    bip32 = BIP32(seed)
    
    # Custom paths
    custom_paths = [
        "m/0'/0'/0'/0",
        "m/44'/0'/0'/0/0",
        "m/49'/0'/0'/0/0",
        "m/84'/0'/0'/0/0",
    ]
    
    for path in custom_paths:
        private_key, public_key, chain_code = bip32.derive_path(path)
        
        # Generate different address types
        p2pkh_addr = BitcoinAddress.p2pkh_address(public_key)
        p2wpkh_p2sh_addr = BitcoinAddress.p2wpkh_p2sh_address(public_key)
        p2wpkh_addr = BitcoinAddress.p2wpkh_address(public_key)
        
        print(f"Path: {path}")
        print(f"  P2PKH (Legacy):     {p2pkh_addr}")
        print(f"  P2WPKH-P2SH:        {p2wpkh_p2sh_addr}")
        print(f"  P2WPKH (SegWit):    {p2wpkh_addr}")
        print()

def main():
    """Run all examples"""
    print("BIP39 Offline Address Generator - Examples")
    print("=" * 50)
    print()
    
    example_1()
    example_2()
    example_3()
    example_4()
    
    print("All examples completed!")

if __name__ == "__main__":
    main()
