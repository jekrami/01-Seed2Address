#!/usr/bin/env python3
"""
Demonstration script showing OpenSSL RIPEMD160 compatibility
This script shows how the code automatically handles different OpenSSL versions
"""

import hashlib
import sys
import os

# Add the current directory to the path so we can import from bip39_offline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bip39_offline import BitcoinAddress, _ripemd160_pure_python, check_ripemd160_availability

def simulate_old_openssl():
    """Simulate an old OpenSSL environment by patching hashlib.new"""
    original_new = hashlib.new
    
    def patched_new(name, *args, **kwargs):
        if name == 'ripemd160':
            raise ValueError("RIPEMD160 is not available in this OpenSSL version")
        return original_new(name, *args, **kwargs)
    
    hashlib.new = patched_new
    return original_new

def restore_hashlib(original_new):
    """Restore original hashlib.new function"""
    hashlib.new = original_new

def demo_compatibility():
    """Demonstrate compatibility with both OpenSSL versions"""
    
    print("OpenSSL RIPEMD160 Compatibility Demonstration")
    print("=" * 60)
    
    # Test data
    test_mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    test_pubkey = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
    
    print(f"Test mnemonic: {test_mnemonic}")
    print(f"Test public key: {test_pubkey.hex()}")
    print()
    
    # Test 1: Current OpenSSL version
    print("1. Testing with current OpenSSL version:")
    print("-" * 40)
    
    ripemd_impl, using_hashlib = check_ripemd160_availability()
    print(f"RIPEMD160 implementation: {ripemd_impl}")
    print(f"OpenSSL version: {getattr(hashlib, 'openssl_version', 'Unknown')}")
    print(f"hashlib ripemd160 available: {using_hashlib}")
    
    # Generate hash160 with current setup
    hash160_current = BitcoinAddress.hash160(test_pubkey)
    print(f"hash160 result: {hash160_current.hex()}")
    
    # Generate a Bitcoin address
    address_current = BitcoinAddress.p2pkh_address(test_pubkey)
    print(f"P2PKH address: {address_current}")
    print()
    
    # Test 2: Simulate old OpenSSL version (RIPEMD160 not available)
    print("2. Simulating old OpenSSL version (RIPEMD160 disabled):")
    print("-" * 40)
    
    # Patch hashlib to simulate old OpenSSL
    original_new = simulate_old_openssl()
    
    try:
        # Check availability again
        ripemd_impl_old, using_hashlib_old = check_ripemd160_availability()
        print(f"RIPEMD160 implementation: {ripemd_impl_old}")
        print(f"hashlib ripemd160 available: {using_hashlib_old}")
        
        # Generate hash160 with fallback
        hash160_fallback = BitcoinAddress.hash160(test_pubkey)
        print(f"hash160 result: {hash160_fallback.hex()}")
        
        # Generate a Bitcoin address
        address_fallback = BitcoinAddress.p2pkh_address(test_pubkey)
        print(f"P2PKH address: {address_fallback}")
        
        # Verify results are identical
        print()
        print("3. Verification:")
        print("-" * 40)
        
        if hash160_current == hash160_fallback:
            print("✅ hash160 results are IDENTICAL")
        else:
            print("❌ hash160 results are DIFFERENT")
            
        if address_current == address_fallback:
            print("✅ Bitcoin addresses are IDENTICAL")
        else:
            print("❌ Bitcoin addresses are DIFFERENT")
            
        print()
        print("This demonstrates that the code produces identical results")
        print("regardless of whether RIPEMD160 is available in OpenSSL or not.")
        
    finally:
        # Restore original hashlib
        restore_hashlib(original_new)
    
    print()
    print("4. Performance comparison:")
    print("-" * 40)
    
    import time
    
    # Test performance of both implementations
    test_data = b"test data for performance comparison" * 100
    iterations = 1000
    
    # Test hashlib implementation (if available)
    if using_hashlib:
        start_time = time.time()
        for _ in range(iterations):
            try:
                h = hashlib.new('ripemd160')
                h.update(test_data)
                h.digest()
            except ValueError:
                break
        hashlib_time = time.time() - start_time
        print(f"hashlib RIPEMD160: {hashlib_time:.4f}s for {iterations} iterations")
    
    # Test pure Python implementation
    start_time = time.time()
    for _ in range(iterations):
        _ripemd160_pure_python(test_data)
    python_time = time.time() - start_time
    print(f"Pure Python RIPEMD160: {python_time:.4f}s for {iterations} iterations")
    
    if using_hashlib:
        speedup = python_time / hashlib_time
        print(f"hashlib is {speedup:.1f}x faster than pure Python")
        print("(This is expected - native implementations are usually faster)")
    
    print()
    print("=" * 60)
    print("CONCLUSION:")
    print("The updated code automatically detects the OpenSSL version and")
    print("uses the appropriate RIPEMD160 implementation, ensuring compatibility")
    print("across different systems while maintaining identical results.")
    print("=" * 60)

if __name__ == "__main__":
    demo_compatibility()
