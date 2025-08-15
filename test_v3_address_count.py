#!/usr/bin/env python3
"""
Test script to verify v3.0 generates correct number of addresses (60 per seed)
"""

def test_address_count():
    """Test that v3.0 generates 60 addresses per seed like v1.0/v2.0"""
    
    print("🧪 Testing v3.0 Address Count Fix")
    print("=" * 50)
    
    # Test mnemonic
    test_mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Expected counts per derivation path (like original)
    expected_counts = {
        "m/44'/0'/0'/0": 10,  # BIP44 - 10 addresses
        "m/49'/0'/0'/0": 10,  # BIP49 - 10 addresses  
        "m/84'/0'/0'/0": 10,  # BIP84 - 10 addresses
        "m/0'/0'/0'": 10,     # Custom - 10 addresses
        "m/0": 20             # Special case - 20 addresses (2 types × 10)
    }
    
    total_expected = sum(expected_counts.values())  # Should be 60
    
    print(f"Test mnemonic: {test_mnemonic}")
    print(f"Expected total addresses: {total_expected}")
    print()
    
    # Test v3.0
    try:
        # Import from the actual file
        import importlib.util
        import os
        v3_file = os.path.join(os.path.dirname(__file__), "batch_process_seeds_g9_v3.0_native.py")
        spec = importlib.util.spec_from_file_location("v3_native", v3_file)
        v3_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(v3_module)

        process_seed_batch_native = v3_module.process_seed_batch_native
        load_wordlist_once = v3_module.load_wordlist_once
        
        # Load wordlist
        wordlist = load_wordlist_once()
        
        # Create test batch
        batch_data = ([test_mnemonic], 10, 0, wordlist)
        
        # Process batch
        results = process_seed_batch_native(batch_data)
        
        # Count results
        successful_results = [r for r in results if r.get('success', False)]
        total_addresses = len(successful_results)
        
        print(f"✅ v3.0 generated {total_addresses} addresses")
        
        # Count by derivation path
        path_counts = {}
        for result in successful_results:
            path = result['derivation_path']
            base_path = None
            
            if path.startswith("m/44'/0'/0'/0/"):
                base_path = "m/44'/0'/0'/0"
            elif path.startswith("m/49'/0'/0'/0/"):
                base_path = "m/49'/0'/0'/0"
            elif path.startswith("m/84'/0'/0'/0/"):
                base_path = "m/84'/0'/0'/0"
            elif path.startswith("m/0'/0'/"):
                base_path = "m/0'/0'/0'"
            elif path.startswith("m/0/"):
                base_path = "m/0"
            
            if base_path:
                path_counts[base_path] = path_counts.get(base_path, 0) + 1
        
        print("\n📊 Address count by derivation path:")
        for path, expected in expected_counts.items():
            actual = path_counts.get(path, 0)
            status = "✅" if actual == expected else "❌"
            print(f"   {status} {path}: {actual}/{expected}")
        
        print(f"\n📊 TOTAL: {total_addresses}/{total_expected}")
        
        if total_addresses == total_expected:
            print("🎉 SUCCESS: v3.0 generates correct number of addresses!")
            
            # Check for m/0 dual addresses
            m0_results = [r for r in successful_results if r['derivation_path'].startswith('m/0/')]
            m0_script_types = set(r['script_semantics'] for r in m0_results)
            
            if "P2WPKH nested in P2SH" in m0_script_types and "P2WPKH" in m0_script_types:
                print("✅ m/0 path correctly generates both P2WPKH nested in P2SH and P2WPKH")
            else:
                print("❌ m/0 path missing dual address types")
                print(f"   Found types: {m0_script_types}")
        else:
            print("❌ FAILED: Incorrect address count")
            print(f"   Expected: {total_expected}")
            print(f"   Actual: {total_addresses}")
            print(f"   Difference: {total_addresses - total_expected}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_address_count()
