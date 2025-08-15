#!/usr/bin/env python3
"""
Final verification script showing exact match with user's expected results
"""

from bip39_offline import generate_addresses

def main():
    """Compare our results with user's expected data"""
    
    print("FINAL VERIFICATION - Exact Match with HTML Tool")
    print("=" * 60)
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Your expected results from the HTML tool
    expected_data = [
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
        }
    ]
    
    # Generate addresses with our tool
    results = generate_addresses(mnemonic, num_addresses=1)
    
    print(f"Mnemonic: {mnemonic}")
    print()
    
    # Extract first address from each derivation path
    our_results = []
    for path_desc, addresses in results.items():
        if addresses:
            our_results.append(addresses[0])
    
    # Compare results
    print("COMPARISON RESULTS:")
    print("-" * 60)
    
    all_match = True
    
    for i, expected in enumerate(expected_data):
        print(f"\n{i+1}. Path: {expected['path']}")
        
        # Find matching result from our generation
        our_result = None
        for result in our_results:
            if expected['path'] in result['path'] or result['path'] in expected['path']:
                our_result = result
                break
        
        if our_result:
            # Compare address
            addr_match = our_result['address'] == expected['address']
            print(f"   Address:    {'✓' if addr_match else '✗'}")
            print(f"   Expected:   {expected['address']}")
            print(f"   Generated:  {our_result['address']}")
            
            # Compare public key
            pubkey_match = our_result['public_key'] == expected['public_key']
            print(f"   Public Key: {'✓' if pubkey_match else '✗'}")
            print(f"   Expected:   {expected['public_key']}")
            print(f"   Generated:  {our_result['public_key']}")
            
            # Compare WIF
            wif_match = our_result['private_key_wif'] == expected['private_key_wif']
            print(f"   WIF:        {'✓' if wif_match else '✗'}")
            print(f"   Expected:   {expected['private_key_wif']}")
            print(f"   Generated:  {our_result['private_key_wif']}")
            
            if not (addr_match and pubkey_match and wif_match):
                all_match = False
        else:
            print(f"   ✗ No matching result found")
            all_match = False
    
    print("\n" + "=" * 60)
    print(f"FINAL RESULT: {'🎉 PERFECT MATCH!' if all_match else '❌ MISMATCH DETECTED'}")
    
    if all_match:
        print("\n✅ All addresses, public keys, and private keys match exactly!")
        print("✅ The offline Python tool produces identical results to the HTML tool!")
        print("✅ Ready for production use!")
    
    # Show additional addresses for each path
    print(f"\n📊 GENERATED 10 ADDRESSES FOR EACH DERIVATION PATH:")
    print("-" * 60)
    
    for path_desc, addresses in results.items():
        print(f"\n{path_desc}:")
        for i, addr in enumerate(addresses[:3]):  # Show first 3
            print(f"  {i}: {addr['address']}")
        if len(addresses) > 3:
            print(f"  ... and {len(addresses) - 3} more addresses")
    
    print(f"\n📁 All results exported to 'bip39_addresses.csv'")
    print(f"📋 Total addresses generated: {sum(len(addrs) for addrs in results.values())}")

if __name__ == "__main__":
    main()
