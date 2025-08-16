#!/usr/bin/env python3
"""
Test script to verify the current implementation against expected results
"""

import sys
import os
import hashlib
import hmac
import struct
import base58

# Add the current directory to path to import from the main script
sys.path.insert(0, '.')

# Import functions from the main script
sys.path.insert(0, '01-Seed2Address')

# Import the module with the correct name
import importlib.util
spec = importlib.util.spec_from_file_location("main_module", "batch_process_seeds_g9_v3.2_optimized.py")
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

derive_key_native = main_module.derive_key_native
generate_address_native = main_module.generate_address_native
NativeCrypto = main_module.NativeCrypto
bech32_encode = main_module.bech32_encode
convertbits = main_module.convertbits

def test_expected_results():
    """Test against the expected results provided by the user"""
    
    # Test data
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    expected_seed = "24bd1b243ec776dd97bc7487ad65c8966ff6e0b8654a25602a41994746957c49c813ba183e6d1646584cf810fcb9898f44571e3ccfe9fb266e3a66597fbcd7c4"
    
    # Expected results for each path
    expected_results = {
        "m/0'/0'/0'": {
            "address": "1GyNWR7LPXdLSHeN4nE4b9P3gNEcjZkmzd",
            "public_key": "0294f267b6174c3694da97f7e554069a7ef475a699753d9c7b568cc35fb0184a4d",
            "private_key_wif": "KyNSzr7jYueYWvsg4cKhwQEmrXCwYmkVAc4qpUX3NU6AqqyNSK7X"
        },
        "m/0'/0'/1'": {
            "address": "1GPruf7qZWTKbAmUH351MAwNpMVqJHjfUT",
            "public_key": "0386bed3c7eac5487da18d35f1712e70a1770efe1b0afede80c79ecadcd39e0cd1",
            "private_key_wif": "L1kzjvx2T4XNxpxVSUvKkCujDNZ1ex5iiRo3uGVEo8wMavEP79pd"
        },
        "m/44'/0'/0'/0/0'": {
            "address": "1Jo3qrSUxWYYJdhDawJ58QU7wtyVtqAK5A",
            "public_key": "0289b86dfa13ad977c57c1a36d94a43b9abe6a62f240e9172556a5ab613208d259",
            "private_key_wif": "L1zvhGE4WoJ1ds17ku9StUqP3x2PH15CUY26DnMgZuMi4jWhoG1w"
        },
        "m/44'/0'/0'/0/1'": {
            "address": "1EhRxsqMeyVTpzYwRBzh2QwfrVcLMBQyYq",
            "public_key": "02ffe750f768a86b9f14bd38bffb20228599db9eb4879f4665aed03c0bb8465c29",
            "private_key_wif": "L4ZfoRrGA9NbrsRCXJupK3kynJnNkbYPPNKgcxtaLHq8hs6yaX4a"
        },
        "m/49'/0'/0'/0/0'": {
            "address": "33ML21FE9QSqh9wizdQbZsHfE41vwkRT78",
            "public_key": "020d92320d95bafbde12605fddf798f3bf99f7f81bcabe8ff1215d0a66603407d6",
            "private_key_wif": "L29EPxkvYEucHGyXz5sHnzmkU9VQQDHG98wB2kMRG5U4Gxmb2PeA"
        },
        "m/49'/0'/0'/0/1'": {
            "address": "33PajXTiRLXvJsSxHnPKZpTRcdWK3HP83h",
            "public_key": "02594db44aa766bcc1cc81c717818085b1940bf43469bd6ee9c3fc8e78ba4f95d5",
            "private_key_wif": "L4LjqJix2A3UVAvRPLbjUFsbM1kHjXJ6T9BxYsH7kYc3mxJNCB6X"
        },
        "m/84'/0'/0'/0/0'": {
            "address": "bc1qnc9umhdc04u0u5qfg0qu3aj75wvfps4z4sj7g6",
            "public_key": "02b0ec1ee8e46c9330f9e23a2eb9576765a8815e858bd4d7d5c492c5d71543fbb4",
            "private_key_wif": "KwpRSjWsMRSaHv45sVFRftZLUJG9jrPM7J474U57ycBFMaxLjJXF"
        },
        "m/84'/0'/0'/0/1'": {
            "address": "bc1q76nvc5jg2zz3uv8pcsjq6h38dvvms5pf3jmw3m",
            "public_key": "03bcbe624058948f696bb3d17c1fe1397672d897d386e5e462f4faaaa2fe19ed93",
            "private_key_wif": "KxSv179DJ1YbCwqxCSbr3fRfi24KCwtUAXof7KVyCitmMvXWqsLq"
        },
        "m/0/0'": {
            "address": "3HWZMAtc7MyENWguyhWaLrLjXpWTMpfZLh",
            "public_key": "028d59eab375e2cbc7de3539c18590f7b1ce121702bfaa5e9e92e2b715549ed283",
            "private_key_wif": "L3V5wXPbC7VmDyh53LUPmYa28yRPz3Vu9Qwmkm6wcU3n8x8aRtDd"
        },
        "m/0/1'": {
            "address": "3FmxkRjhFeCtoQdeYU2ubGB4NsnUGFMEFJ",
            "public_key": "0233ec633bbd7eaa6a2535a265b8ee8d422343c943454f72150d47a58b95af2097",
            "private_key_wif": "L4SqZuiDs6m5tTfGMZT5ZX5hfPKqhP2DZZT1zbBtcLavan7TJH71"
        }
    }
    
    print("Testing BIP39 seed generation...")
    
    # Generate seed
    mnemonic_bytes = mnemonic.encode('utf-8')
    salt = b'mnemonic'
    seed_bytes = NativeCrypto.pbkdf2_native(mnemonic_bytes, salt, 2048)
    generated_seed = seed_bytes.hex()
    
    print(f"Expected seed: {expected_seed}")
    print(f"Generated seed: {generated_seed}")
    print(f"Seed match: {generated_seed == expected_seed}")
    print()
    
    if generated_seed != expected_seed:
        print("❌ SEED GENERATION FAILED!")
        return False
    
    print("✅ Seed generation correct!")
    print()
    
    # Test each derivation path
    all_correct = True
    
    for path, expected in expected_results.items():
        print(f"Testing path: {path}")
        
        try:
            # Derive key
            private_key, public_key = derive_key_native(seed_bytes, path)
            
            # Generate WIF
            version_byte = 0x80
            extended_key = bytes([version_byte]) + private_key + bytes([0x01])
            checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
            private_key_wif = base58.b58encode(extended_key + checksum).decode('ascii')
            
            # Determine address type based on path
            if path.startswith("m/44'"):
                address_type = "P2PKH"
            elif path.startswith("m/49'"):
                address_type = "P2WPKH nested in P2SH"
            elif path.startswith("m/84'"):
                address_type = "P2WPKH"
            elif path.startswith("m/0'"):
                address_type = "P2PKH"
            elif path.startswith("m/0/") and path.endswith("'"):
                address_type = "P2WPKH nested in P2SH"
            else:
                address_type = "P2PKH"
            
            # Generate address
            address = generate_address_native(public_key, address_type)
            
            # Compare results
            public_key_hex = public_key.hex()
            
            print(f"  Expected address: {expected['address']}")
            print(f"  Generated address: {address}")
            print(f"  Address match: {address == expected['address']}")
            
            print(f"  Expected public key: {expected['public_key']}")
            print(f"  Generated public key: {public_key_hex}")
            print(f"  Public key match: {public_key_hex == expected['public_key']}")
            
            print(f"  Expected WIF: {expected['private_key_wif']}")
            print(f"  Generated WIF: {private_key_wif}")
            print(f"  WIF match: {private_key_wif == expected['private_key_wif']}")
            
            if (address != expected['address'] or 
                public_key_hex != expected['public_key'] or 
                private_key_wif != expected['private_key_wif']):
                print(f"  ❌ MISMATCH for path {path}")
                all_correct = False
            else:
                print(f"  ✅ CORRECT for path {path}")
            
            print()
            
        except Exception as e:
            print(f"  ❌ ERROR for path {path}: {e}")
            all_correct = False
            print()
    
    return all_correct

if __name__ == "__main__":
    success = test_expected_results()
    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    sys.exit(0 if success else 1)
