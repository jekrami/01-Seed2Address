#!/usr/bin/env python3
"""
Test script to verify our implementation against the exact expected results
provided by the user from the HTML tool
"""

from bip39_offline import BIP39, BIP32, BitcoinAddress

def test_specific_paths():
    """Test the specific paths and expected results from the user"""
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Expected results from user
    expected_results = [
        {
            "path": "m/0'/0'/0'",
            "address": "1GyNWR7LPXdLSHeN4nE4b9P3gNEcjZkmzd",
            "public_key": "0294f267b6174c3694da97f7e554069a7ef475a699753d9c7b568cc35fb0184a4d",
            "private_key_wif": "KyNSzr7jYueYWvsg4cKhwQEmrXCwYmkVAc4qpUX3NU6AqqyNSK7X"
        },
        {
            "path": "m/44'/0'/0'/0/0'",
            "address": "1Jo3qrSUxWYYJdhDawJ58QU7wtyVtqAK5A",
            "public_key": "0289b86dfa13ad977c57c1a36d94a43b9abe6a62f240e9172556a5ab613208d259",
            "private_key_wif": "L1zvhGE4WoJ1ds17ku9StUqP3x2PH15CUY26DnMgZuMi4jWhoG1w"
        },
        {
            "path": "m/49'/0'/0'/0/0'",
            "address": "33ML21FE9QSqh9wizdQbZsHfE41vwkRT78",
            "public_key": "020d92320d95bafbde12605fddf798f3bf99f7f81bcabe8ff1215d0a66603407d6",
            "private_key_wif": "L29EPxkvYEucHGyXz5sHnzmkU9VQQDHG98wB2kMRG5U4Gxmb2PeA"
        },
        {
            "path": "m/84'/0'/0'/0/0'",
            "address": "bc1qnc9umhdc04u0u5qfg0qu3aj75wvfps4z4sj7g6",
            "public_key": "02b0ec1ee8e46c9330f9e23a2eb9576765a8815e858bd4d7d5c492c5d71543fbb4",
            "private_key_wif": "KwpRSjWsMRSaHv45sVFRftZLUJG9jrPM7J474U57ycBFMaxLjJXF"
        },
        {
            "path": "m/0/0'",
            "address_p2sh": "3HWZMAtc7MyENWguyhWaLrLjXpWTMpfZLh",
            "address_p2wpkh": "bc1qe59ssevhzy9v76syff0508ml97xm0rstcfdw0y",
            "public_key": "028d59eab375e2cbc7de3539c18590f7b1ce121702bfaa5e9e92e2b715549ed283",
            "private_key_wif": "L3V5wXPbC7VmDyh53LUPmYa28yRPz3Vu9Qwmkm6wcU3n8x8aRtDd"
        }
    ]
    
    print("Testing Specific Expected Results")
    print("=" * 50)
    
    # Initialize BIP39 and BIP32
    bip39 = BIP39()
    seed = bip39.mnemonic_to_seed(mnemonic)
    bip32 = BIP32(seed)
    
    all_passed = True
    
    for i, expected in enumerate(expected_results):
        print(f"\nTest {i+1}: {expected['path']}")
        print("-" * 30)
        
        try:
            # Handle the special case of m/0/0' (hardened)
            if expected['path'] == "m/0/0'":
                # This is m/0/0 with hardened derivation
                private_key, public_key, chain_code = bip32.derive_path("m/0/0'")
            else:
                # Regular path
                private_key, public_key, chain_code = bip32.derive_path(expected['path'])
            
            # Generate addresses
            if "44'" in expected['path']:
                address = BitcoinAddress.p2pkh_address(public_key)
            elif "49'" in expected['path']:
                address = BitcoinAddress.p2wpkh_p2sh_address(public_key)
            elif "84'" in expected['path']:
                address = BitcoinAddress.p2wpkh_address(public_key)
            else:
                address = BitcoinAddress.p2pkh_address(public_key)
            
            # Convert to WIF
            private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)
            
            # Check results
            public_key_hex = public_key.hex()
            
            print(f"Expected Address: {expected.get('address', 'N/A')}")
            print(f"Generated Address: {address}")
            
            if 'address' in expected:
                address_match = address == expected['address']
                print(f"Address Match: {'✓' if address_match else '✗'}")
                if not address_match:
                    all_passed = False
            
            print(f"Expected PubKey: {expected['public_key']}")
            print(f"Generated PubKey: {public_key_hex}")
            pubkey_match = public_key_hex == expected['public_key']
            print(f"PubKey Match: {'✓' if pubkey_match else '✗'}")
            if not pubkey_match:
                all_passed = False
            
            print(f"Expected WIF: {expected['private_key_wif']}")
            print(f"Generated WIF: {private_key_wif}")
            wif_match = private_key_wif == expected['private_key_wif']
            print(f"WIF Match: {'✓' if wif_match else '✗'}")
            if not wif_match:
                all_passed = False
            
            # For the special case with multiple address types
            if 'address_p2sh' in expected:
                p2sh_addr = BitcoinAddress.p2wpkh_p2sh_address(public_key)
                p2wpkh_addr = BitcoinAddress.p2wpkh_address(public_key)
                
                print(f"Expected P2SH: {expected['address_p2sh']}")
                print(f"Generated P2SH: {p2sh_addr}")
                p2sh_match = p2sh_addr == expected['address_p2sh']
                print(f"P2SH Match: {'✓' if p2sh_match else '✗'}")
                
                print(f"Expected P2WPKH: {expected['address_p2wpkh']}")
                print(f"Generated P2WPKH: {p2wpkh_addr}")
                p2wpkh_match = p2wpkh_addr == expected['address_p2wpkh']
                print(f"P2WPKH Match: {'✓' if p2wpkh_match else '✗'}")
                
                if not (p2sh_match and p2wpkh_match):
                    all_passed = False
                    
        except Exception as e:
            print(f"Error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    print(f"OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

def debug_derivation():
    """Debug the derivation process step by step"""
    
    print("\nDEBUG: Step-by-step derivation")
    print("=" * 40)
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    bip39 = BIP39()
    seed = bip39.mnemonic_to_seed(mnemonic)
    bip32 = BIP32(seed)
    
    # Test the problematic path m/0'/0'/0'
    print("\nDebugging m/0'/0'/0':")
    
    # Step 1: m/0'
    step1_key, step1_pub, step1_chain = bip32.derive_path("m/0'")
    print(f"m/0' private key: {step1_key.hex()}")
    print(f"m/0' public key: {step1_pub.hex()}")
    
    # Step 2: m/0'/0'
    step2_key, step2_pub, step2_chain = bip32.derive_path("m/0'/0'")
    print(f"m/0'/0' private key: {step2_key.hex()}")
    print(f"m/0'/0' public key: {step2_pub.hex()}")
    
    # Step 3: m/0'/0'/0'
    step3_key, step3_pub, step3_chain = bip32.derive_path("m/0'/0'/0'")
    print(f"m/0'/0'/0' private key: {step3_key.hex()}")
    print(f"m/0'/0'/0' public key: {step3_pub.hex()}")
    
    # Generate address
    address = BitcoinAddress.p2pkh_address(step3_pub)
    wif = BitcoinAddress.private_key_to_wif(step3_key, compressed=True)
    
    print(f"Generated address: {address}")
    print(f"Generated WIF: {wif}")
    print(f"Expected address: 1GyNWR7LPXdLSHeN4nE4b9P3gNEcjZkmzd")
    print(f"Expected WIF: KyNSzr7jYueYWvsg4cKhwQEmrXCwYmkVAc4qpUX3NU6AqqyNSK7X")

if __name__ == "__main__":
    success = test_specific_paths()
    debug_derivation()
    
    if not success:
        print("\n⚠️ Tests failed. The implementation needs adjustment to match the HTML tool exactly.")
