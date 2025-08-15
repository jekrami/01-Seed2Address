#!/usr/bin/env python3
"""
Test the new pattern based on the latest sample data from the user
"""

from bip39_offline import generate_addresses

def test_new_pattern():
    """Test against the new sample data provided by the user"""
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Expected results from the latest user sample
    expected_results = [
        # m/0'/0'/X' pattern
        {"path": "m/0'/0'/0'", "address": "1GyNWR7LPXdLSHeN4nE4b9P3gNEcjZkmzd", "public_key": "0294f267b6174c3694da97f7e554069a7ef475a699753d9c7b568cc35fb0184a4d", "wif": "KyNSzr7jYueYWvsg4cKhwQEmrXCwYmkVAc4qpUX3NU6AqqyNSK7X"},
        {"path": "m/0'/0'/1'", "address": "1GPruf7qZWTKbAmUH351MAwNpMVqJHjfUT", "public_key": "0386bed3c7eac5487da18d35f1712e70a1770efe1b0afede80c79ecadcd39e0cd1", "wif": "L1kzjvx2T4XNxpxVSUvKkCujDNZ1ex5iiRo3uGVEo8wMavEP79pd"},
        
        # m/44'/0'/0'/0/X' pattern
        {"path": "m/44'/0'/0'/0/0'", "address": "1Jo3qrSUxWYYJdhDawJ58QU7wtyVtqAK5A", "public_key": "0289b86dfa13ad977c57c1a36d94a43b9abe6a62f240e9172556a5ab613208d259", "wif": "L1zvhGE4WoJ1ds17ku9StUqP3x2PH15CUY26DnMgZuMi4jWhoG1w"},
        {"path": "m/44'/0'/0'/0/1'", "address": "1EhRxsqMeyVTpzYwRBzh2QwfrVcLMBQyYq", "public_key": "02ffe750f768a86b9f14bd38bffb20228599db9eb4879f4665aed03c0bb8465c29", "wif": "L4ZfoRrGA9NbrsRCXJupK3kynJnNkbYPPNKgcxtaLHq8hs6yaX4a"},
        
        # m/49'/0'/0'/0/X' pattern
        {"path": "m/49'/0'/0'/0/0'", "address": "33ML21FE9QSqh9wizdQbZsHfE41vwkRT78", "public_key": "020d92320d95bafbde12605fddf798f3bf99f7f81bcabe8ff1215d0a66603407d6", "wif": "L29EPxkvYEucHGyXz5sHnzmkU9VQQDHG98wB2kMRG5U4Gxmb2PeA"},
        {"path": "m/49'/0'/0'/0/1'", "address": "33PajXTiRLXvJsSxHnPKZpTRcdWK3HP83h", "public_key": "02594db44aa766bcc1cc81c717818085b1940bf43469bd6ee9c3fc8e78ba4f95d5", "wif": "L4LjqJix2A3UVAvRPLbjUFsbM1kHjXJ6T9BxYsH7kYc3mxJNCB6X"},
        
        # m/84'/0'/0'/0/X' pattern
        {"path": "m/84'/0'/0'/0/0'", "address": "bc1qnc9umhdc04u0u5qfg0qu3aj75wvfps4z4sj7g6", "public_key": "02b0ec1ee8e46c9330f9e23a2eb9576765a8815e858bd4d7d5c492c5d71543fbb4", "wif": "KwpRSjWsMRSaHv45sVFRftZLUJG9jrPM7J474U57ycBFMaxLjJXF"},
        {"path": "m/84'/0'/0'/0/1'", "address": "bc1q76nvc5jg2zz3uv8pcsjq6h38dvvms5pf3jmw3m", "public_key": "03bcbe624058948f696bb3d17c1fe1397672d897d386e5e462f4faaaa2fe19ed93", "wif": "KxSv179DJ1YbCwqxCSbr3fRfi24KCwtUAXof7KVyCitmMvXWqsLq"},
        
        # m/0/X' pattern (P2SH and P2WPKH)
        {"path": "m/0/0'", "address_p2sh": "3HWZMAtc7MyENWguyhWaLrLjXpWTMpfZLh", "address_p2wpkh": "bc1qe59ssevhzy9v76syff0508ml97xm0rstcfdw0y", "public_key": "028d59eab375e2cbc7de3539c18590f7b1ce121702bfaa5e9e92e2b715549ed283", "wif": "L3V5wXPbC7VmDyh53LUPmYa28yRPz3Vu9Qwmkm6wcU3n8x8aRtDd"},
        {"path": "m/0/1'", "address_p2sh": "3FmxkRjhFeCtoQdeYU2ubGB4NsnUGFMEFJ", "address_p2wpkh": "bc1qavf2aluhaehmx8jc2nf2jz23enuh9m6esmxzy8", "public_key": "0233ec633bbd7eaa6a2535a265b8ee8d422343c943454f72150d47a58b95af2097", "wif": "L4SqZuiDs6m5tTfGMZT5ZX5hfPKqhP2DZZT1zbBtcLavan7TJH71"},
    ]
    
    print("Testing New Pattern Based on Latest Sample Data")
    print("=" * 60)
    
    # Generate addresses with our updated tool
    results = generate_addresses(mnemonic, num_addresses=2)  # Generate 2 addresses per path
    
    # Flatten results for easier comparison
    our_addresses = []
    for path_desc, addresses in results.items():
        our_addresses.extend(addresses)
    
    print(f"Generated {len(our_addresses)} addresses")
    print(f"Expected {len(expected_results)} test cases")
    print()
    
    all_passed = True
    
    for i, expected in enumerate(expected_results):
        print(f"Test {i+1}: {expected['path']}")
        print("-" * 40)
        
        # Find matching address in our results
        our_result = None
        for addr in our_addresses:
            if addr['path'] == expected['path']:
                our_result = addr
                break
        
        if our_result:
            # Test address
            if 'address' in expected:
                addr_match = our_result['address'] == expected['address']
                print(f"Address:    {'✓' if addr_match else '✗'}")
                print(f"Expected:   {expected['address']}")
                print(f"Generated:  {our_result['address']}")
                if not addr_match:
                    all_passed = False
            
            # Test public key
            pubkey_match = our_result['public_key'] == expected['public_key']
            print(f"Public Key: {'✓' if pubkey_match else '✗'}")
            print(f"Expected:   {expected['public_key']}")
            print(f"Generated:  {our_result['public_key']}")
            if not pubkey_match:
                all_passed = False
            
            # Test WIF
            wif_match = our_result['private_key_wif'] == expected['wif']
            print(f"WIF:        {'✓' if wif_match else '✗'}")
            print(f"Expected:   {expected['wif']}")
            print(f"Generated:  {our_result['private_key_wif']}")
            if not wif_match:
                all_passed = False
            
            # Test additional address types for m/0/X' paths
            if 'address_p2sh' in expected:
                from bip39_offline import BitcoinAddress, BIP32, BIP39
                
                # Generate both address types for comparison
                bip39 = BIP39()
                seed = bip39.mnemonic_to_seed(mnemonic)
                bip32 = BIP32(seed)
                private_key, public_key, _ = bip32.derive_path(expected['path'])
                
                p2sh_addr = BitcoinAddress.p2wpkh_p2sh_address(public_key)
                p2wpkh_addr = BitcoinAddress.p2wpkh_address(public_key)
                
                p2sh_match = p2sh_addr == expected['address_p2sh']
                p2wpkh_match = p2wpkh_addr == expected['address_p2wpkh']
                
                print(f"P2SH:       {'✓' if p2sh_match else '✗'}")
                print(f"Expected:   {expected['address_p2sh']}")
                print(f"Generated:  {p2sh_addr}")
                
                print(f"P2WPKH:     {'✓' if p2wpkh_match else '✗'}")
                print(f"Expected:   {expected['address_p2wpkh']}")
                print(f"Generated:  {p2wpkh_addr}")
                
                if not (p2sh_match and p2wpkh_match):
                    all_passed = False
        else:
            print(f"✗ No matching result found for path {expected['path']}")
            all_passed = False
        
        print()
    
    print("=" * 60)
    print(f"RESULT: {'🎉 ALL TESTS PASSED!' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("✅ The new pattern implementation is working correctly!")
        print("✅ All addresses, public keys, and WIF keys match exactly!")
    else:
        print("⚠️ Some tests failed. Need to adjust the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_new_pattern()
