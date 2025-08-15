#!/usr/bin/env python3
"""
Verification script to compare our BIP39 implementation results
with the expected data provided by the user
"""

from bip39_offline import BIP39, generate_addresses

def verify_test_data():
    """Verify our implementation against the test data"""
    
    # Test data from user
    test_mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    expected_seed = "24bd1b243ec776dd97bc7487ad65c8966ff6e0b8654a25602a41994746957c49c813ba183e6d1646584cf810fcb9898f44571e3ccfe9fb266e3a66597fbcd7c4"
    
    print("BIP39 Offline Tool Verification")
    print("=" * 40)
    print()
    
    # Test 1: Seed Generation
    print("Test 1: Seed Generation")
    print("-" * 25)
    bip39 = BIP39()
    generated_seed = bip39.mnemonic_to_seed(test_mnemonic).hex()
    
    print(f"Expected:  {expected_seed}")
    print(f"Generated: {generated_seed}")
    print(f"✓ Seed Match: {generated_seed == expected_seed}")
    print()
    
    # Test 2: Mnemonic Validation
    print("Test 2: Mnemonic Validation")
    print("-" * 28)
    is_valid = bip39.validate_mnemonic(test_mnemonic)
    print(f"Mnemonic: {test_mnemonic}")
    print(f"✓ Valid: {is_valid}")
    print()
    
    # Test 3: Address Generation
    print("Test 3: Address Generation")
    print("-" * 27)
    results = generate_addresses(test_mnemonic, num_addresses=1)
    
    # Expected first addresses for each path type
    expected_addresses = {
        "m/0'/0'/0'": "1C8cV6JmBuXYLtXk44uwkgaBGdLEzG7uGf",  # Legacy Custom
        "m/44'/0'/0'/0": "1LDXHEixXvhQyVRHCN1fSHYCQUbHbPsPsq",  # BIP44
        "m/49'/0'/0'/0": "3MMpkkGYLvU7mjMfrfZZJat9sbWG37zgiN",  # BIP49
        "m/84'/0'/0'/0": "bc1qfnzvskgpv97fm7ewrmfgsymdf3wr47w4pguwua",  # BIP84
        "m/0": "1Dr8VVeTm9JFNP87DvThQHH1ajPaG6UCHU",  # Simple
    }
    
    all_correct = True
    
    for path_desc, addresses in results.items():
        if addresses:
            first_addr = addresses[0]
            path = first_addr['path']
            generated_addr = first_addr['address']
            
            # Find expected address for this path
            expected_addr = None
            for exp_path, exp_addr in expected_addresses.items():
                if exp_path in path:
                    expected_addr = exp_addr
                    break
            
            if expected_addr:
                match = generated_addr == expected_addr
                all_correct = all_correct and match
                status = "✓" if match else "✗"
                
                print(f"{status} {path}")
                print(f"  Expected:  {expected_addr}")
                print(f"  Generated: {generated_addr}")
                if not match:
                    print(f"  ❌ MISMATCH!")
                print()
    
    # Test 4: Multiple Address Generation
    print("Test 4: Multiple Address Generation")
    print("-" * 35)
    results_10 = generate_addresses(test_mnemonic, num_addresses=10)
    
    total_addresses = sum(len(addrs) for addrs in results_10.values())
    expected_total = 5 * 10  # 5 derivation paths × 10 addresses each
    
    print(f"Generated {total_addresses} addresses across {len(results_10)} derivation paths")
    print(f"Expected: {expected_total} addresses")
    print(f"✓ Count Match: {total_addresses == expected_total}")
    print()
    
    # Summary
    print("=" * 40)
    print("VERIFICATION SUMMARY")
    print("=" * 40)
    print(f"✓ Seed generation: {'PASS' if generated_seed == expected_seed else 'FAIL'}")
    print(f"✓ Mnemonic validation: {'PASS' if is_valid else 'FAIL'}")
    print(f"✓ Address generation: {'PASS' if all_correct else 'FAIL'}")
    print(f"✓ Multiple addresses: {'PASS' if total_addresses == expected_total else 'FAIL'}")
    
    overall_pass = (generated_seed == expected_seed and is_valid and 
                   all_correct and total_addresses == expected_total)
    
    print()
    print(f"🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_pass else '❌ SOME TESTS FAILED'}")
    
    return overall_pass

def compare_with_original_html():
    """Compare specific derivation paths mentioned in the user's request"""
    
    print("\n" + "=" * 60)
    print("COMPARISON WITH ORIGINAL HTML TOOL")
    print("=" * 60)
    
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # User's specified paths and expected results
    user_paths = [
        "m/0'/0'/0'",
        "m/44'/0'/0'/0/0'",  # Note: This seems to have an extra apostrophe
        "m/49'/0'/0'/0/0'",  # Note: This seems to have an extra apostrophe  
        "m/84'/0'/0'/0/0'",  # Note: This seems to have an extra apostrophe
        "m/0/0'",           # Note: This seems to have an apostrophe
    ]
    
    print("User's requested derivation paths:")
    for path in user_paths:
        print(f"  - {path}")
    
    print("\nNote: Some paths in the user's request have unusual apostrophe placement.")
    print("Our implementation uses standard BIP32 notation.")
    print("\nGenerated addresses for standard paths:")
    
    results = generate_addresses(mnemonic, num_addresses=1)
    
    for path_desc, addresses in results.items():
        if addresses:
            addr_info = addresses[0]
            print(f"\n{path_desc}")
            print(f"  Path: {addr_info['path']}")
            print(f"  Address: {addr_info['address']}")
            print(f"  Script: {addr_info['script_semantics']}")

if __name__ == "__main__":
    success = verify_test_data()
    compare_with_original_html()
    
    if success:
        print("\n🎉 All verifications passed! The offline tool is working correctly.")
    else:
        print("\n⚠️  Some verifications failed. Please check the implementation.")
