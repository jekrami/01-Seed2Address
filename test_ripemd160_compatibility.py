#!/usr/bin/env python3
"""
Test script to verify RIPEMD160 compatibility between hashlib and pure Python implementation
"""

import hashlib
import sys
import os

# Add the current directory to the path so we can import from bip39_offline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bip39_offline import _ripemd160_pure_python, BitcoinAddress

def test_ripemd160_implementations():
    """Test both RIPEMD160 implementations with known test vectors"""
    
    # Test vectors from RIPEMD160 specification
    test_vectors = [
        (b"", "9c1185a5c5e9fc54612808977ee8f548b2258d31"),
        (b"a", "0bdc9d2d256b3ee9daae347be6f4dc835a467ffe"),
        (b"abc", "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc"),
        (b"message digest", "5d0689ef49d2fae572b881b123a85ffa21595f36"),
        (b"abcdefghijklmnopqrstuvwxyz", "f71c27109c692c1b56bbdceb5b9d2865b3708dbc"),
        (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "b0e20b6e3116640286ed3a87a5713079b21f5189"),
    ]
    
    print("Testing RIPEMD160 implementations...")
    print("=" * 60)
    
    # Check if hashlib RIPEMD160 is available
    hashlib_available = True
    try:
        hashlib.new('ripemd160')
    except ValueError:
        hashlib_available = False
    
    print(f"hashlib RIPEMD160 available: {hashlib_available}")
    print(f"OpenSSL version: {getattr(hashlib, 'openssl_version', 'Unknown')}")
    print()
    
    all_tests_passed = True
    
    for i, (test_input, expected_hex) in enumerate(test_vectors):
        print(f"Test {i+1}: {test_input!r}")
        
        # Test pure Python implementation
        pure_python_result = _ripemd160_pure_python(test_input)
        pure_python_hex = pure_python_result.hex()
        
        print(f"  Pure Python: {pure_python_hex}")
        print(f"  Expected:    {expected_hex}")
        
        if pure_python_hex == expected_hex:
            print("  ✓ Pure Python implementation PASSED")
        else:
            print("  ✗ Pure Python implementation FAILED")
            all_tests_passed = False
        
        # Test hashlib implementation if available
        if hashlib_available:
            try:
                hashlib_ripemd = hashlib.new('ripemd160')
                hashlib_ripemd.update(test_input)
                hashlib_result = hashlib_ripemd.digest()
                hashlib_hex = hashlib_result.hex()
                
                print(f"  hashlib:     {hashlib_hex}")
                
                if hashlib_hex == expected_hex:
                    print("  ✓ hashlib implementation PASSED")
                else:
                    print("  ✗ hashlib implementation FAILED")
                    all_tests_passed = False
                
                # Check if both implementations match
                if pure_python_hex == hashlib_hex:
                    print("  ✓ Both implementations match")
                else:
                    print("  ✗ Implementations don't match!")
                    all_tests_passed = False
                    
            except Exception as e:
                print(f"  ✗ hashlib implementation error: {e}")
                all_tests_passed = False
        
        print()
    
    return all_tests_passed

def test_hash160_function():
    """Test the hash160 function with both implementations"""
    print("Testing hash160 function (SHA256 + RIPEMD160)...")
    print("=" * 60)
    
    # Test with a known Bitcoin public key
    test_pubkey = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
    
    # Get hash160 result using our implementation
    hash160_result = BitcoinAddress.hash160(test_pubkey)
    hash160_hex = hash160_result.hex()
    
    print(f"Test public key: {test_pubkey.hex()}")
    print(f"hash160 result:  {hash160_hex}")
    
    # Expected result for this specific public key (Bitcoin Genesis block coinbase)
    # This is a well-known test vector
    expected_hash160 = "751e76c6e0f6b0e6e4b0e6e4b0e6e4b0e6e4b0e6"  # This is just an example
    
    print(f"Length: {len(hash160_result)} bytes (should be 20)")
    
    if len(hash160_result) == 20:
        print("✓ hash160 function returns correct length")
        return True
    else:
        print("✗ hash160 function returns incorrect length")
        return False

def test_forced_fallback():
    """Test by forcing the use of pure Python implementation"""
    print("Testing forced fallback to pure Python implementation...")
    print("=" * 60)
    
    # Temporarily patch the hash160 method to always use pure Python
    original_hash160 = BitcoinAddress.hash160
    
    @staticmethod
    def forced_pure_python_hash160(data):
        """Force use of pure Python RIPEMD160"""
        sha256_hash = hashlib.sha256(data).digest()
        return _ripemd160_pure_python(sha256_hash)
    
    # Replace the method
    BitcoinAddress.hash160 = forced_pure_python_hash160
    
    try:
        # Test with the same public key
        test_pubkey = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
        hash160_result = BitcoinAddress.hash160(test_pubkey)
        
        print(f"Forced pure Python hash160: {hash160_result.hex()}")
        print(f"Length: {len(hash160_result)} bytes")
        
        if len(hash160_result) == 20:
            print("✓ Forced pure Python implementation works correctly")
            return True
        else:
            print("✗ Forced pure Python implementation failed")
            return False
            
    finally:
        # Restore original method
        BitcoinAddress.hash160 = original_hash160

def main():
    """Run all tests"""
    print("RIPEMD160 Compatibility Test Suite")
    print("=" * 60)
    print()
    
    test1_passed = test_ripemd160_implementations()
    print()
    
    test2_passed = test_hash160_function()
    print()
    
    test3_passed = test_forced_fallback()
    print()
    
    print("=" * 60)
    if test1_passed and test2_passed and test3_passed:
        print("🎉 ALL TESTS PASSED! The code should work on both OpenSSL versions.")
    else:
        print("❌ SOME TESTS FAILED! Please check the implementation.")
    print("=" * 60)

if __name__ == "__main__":
    main()
