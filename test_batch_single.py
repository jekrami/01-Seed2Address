#!/usr/bin/env python3
"""
Test the batch processing with a single seed to verify the fix
"""

import importlib.util
import csv

# Import the module
spec = importlib.util.spec_from_file_location("main_module", "batch_process_seeds_g9_v3.2_optimized.py")
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

def test_batch_processing():
    """Test batch processing with the expected mnemonic"""
    
    # Test data
    mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    
    # Load wordlist
    wordlist = main_module.load_wordlist_once()
    
    # Create batch data (seeds, num_addresses, start_idx, wordlist)
    batch_data = ([mnemonic], 2, 0, wordlist)  # Generate 2 addresses per path
    
    # Process the batch
    results = main_module.process_seed_batch_native(batch_data)
    
    # Filter successful results
    successful = [r for r in results if r.get('success', False)]
    
    print(f"Generated {len(successful)} results:")
    print()
    
    # Group by derivation path
    by_path = {}
    for result in successful:
        path = result['derivation_path']
        if path not in by_path:
            by_path[path] = []
        by_path[path].append(result)
    
    # Print results organized by path
    for path in sorted(by_path.keys()):
        results_for_path = by_path[path]
        print(f"Path: {path}")
        print(f"Script Semantics: {results_for_path[0]['script_semantics']}")
        print()
        
        for result in results_for_path:
            print(f"  Address {result['address_index']}: {result['address']}")
            print(f"  Public Key: {result['public_key']}")
            print(f"  Private Key WIF: {result['private_key_wif']}")
            print()
        
        print("-" * 80)
        print()

if __name__ == "__main__":
    test_batch_processing()
