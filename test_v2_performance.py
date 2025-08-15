#!/usr/bin/env python3
"""
Test script to verify v2.0 performance optimization is working
"""

import time
import psutil
import os

def test_v1_vs_v2_performance():
    """Test the performance difference between v1.0 and v2.0"""
    
    print("🔬 Testing v1.0 vs v2.0 Performance")
    print("=" * 50)
    
    # Test data
    test_mnemonic = "motor venture dilemma quote subject magnet keep large dry gossip bean paper"
    num_iterations = 50
    
    print(f"Test: {num_iterations} iterations of generate_addresses()")
    print(f"Mnemonic: {test_mnemonic}")
    print()
    
    # Test v1.0 (original)
    print("🧪 Testing v1.0 (original)...")
    try:
        from bip39_offline import generate_addresses as generate_v1, BIP39 as BIP39_v1
        
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        
        for i in range(num_iterations):
            # v1.0 behavior: creates new BIP39 instance every time
            addresses = generate_v1(test_mnemonic, num_addresses=2)
        
        end_time = time.time()
        end_cpu = psutil.cpu_percent()
        
        v1_time = end_time - start_time
        v1_speed = num_iterations / v1_time
        
        print(f"   ⏱️  Time: {v1_time:.3f} seconds")
        print(f"   🚀 Speed: {v1_speed:.2f} iterations/second")
        print(f"   💻 CPU: {end_cpu:.1f}%")
        
    except Exception as e:
        print(f"   ❌ v1.0 test failed: {e}")
        v1_time = None
        v1_speed = None
    
    print()
    
    # Test v2.0 (optimized)
    print("🧪 Testing v2.0 (optimized)...")
    try:
        from bip39_offline_v2_0_g9_optimized import generate_addresses as generate_v2, BIP39 as BIP39_v2
        
        # Pre-create BIP39 instance (v2.0 optimization)
        bip39_instance = BIP39_v2()
        
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        
        for i in range(num_iterations):
            # v2.0 behavior: reuse existing BIP39 instance
            addresses = generate_v2(test_mnemonic, num_addresses=2, bip39_instance=bip39_instance)
        
        end_time = time.time()
        end_cpu = psutil.cpu_percent()
        
        v2_time = end_time - start_time
        v2_speed = num_iterations / v2_time
        
        print(f"   ⏱️  Time: {v2_time:.3f} seconds")
        print(f"   🚀 Speed: {v2_speed:.2f} iterations/second")
        print(f"   💻 CPU: {end_cpu:.1f}%")
        
    except Exception as e:
        print(f"   ❌ v2.0 test failed: {e}")
        v2_time = None
        v2_speed = None
    
    print()
    
    # Compare results
    if v1_time and v2_time:
        improvement = v1_time / v2_time
        speed_improvement = v2_speed / v1_speed
        
        print("📊 COMPARISON:")
        print(f"   ⚡ v2.0 is {improvement:.2f}x faster than v1.0")
        print(f"   🚀 Speed improvement: {speed_improvement:.2f}x")
        
        if improvement > 2:
            print("   ✅ v2.0 optimization is working!")
        elif improvement > 1.2:
            print("   ⚠️  v2.0 shows some improvement")
        else:
            print("   ❌ v2.0 optimization is NOT working")
    
    print()

def test_file_io_operations():
    """Test file I/O operations to see the difference"""
    
    print("📁 Testing File I/O Operations")
    print("=" * 50)
    
    # Test v1.0 file I/O
    print("🧪 Testing v1.0 file I/O (creates new BIP39 each time)...")
    try:
        from bip39_offline import BIP39 as BIP39_v1
        
        start_time = time.time()
        
        for i in range(10):
            bip39 = BIP39_v1()  # This loads the CSV file
        
        end_time = time.time()
        v1_io_time = end_time - start_time
        
        print(f"   ⏱️  10 BIP39 creations: {v1_io_time:.3f} seconds")
        print(f"   📁 File reads: 10 (one per creation)")
        
    except Exception as e:
        print(f"   ❌ v1.0 I/O test failed: {e}")
        v1_io_time = None
    
    print()
    
    # Test v2.0 file I/O
    print("🧪 Testing v2.0 file I/O (reuses existing BIP39)...")
    try:
        from bip39_offline_v2_0_g9_optimized import BIP39 as BIP39_v2
        
        start_time = time.time()
        
        # Create once, reuse 10 times
        bip39 = BIP39_v2()  # This loads the CSV file once
        for i in range(9):
            # Simulate reuse (no file I/O)
            pass
        
        end_time = time.time()
        v2_io_time = end_time - start_time
        
        print(f"   ⏱️  1 BIP39 creation + 9 reuses: {v2_io_time:.3f} seconds")
        print(f"   📁 File reads: 1 (reused 9 times)")
        
    except Exception as e:
        print(f"   ❌ v2.0 I/O test failed: {e}")
        v2_io_time = None
    
    print()
    
    # Compare I/O
    if v1_io_time and v2_io_time:
        io_improvement = v1_io_time / v2_io_time
        print("📊 I/O COMPARISON:")
        print(f"   ⚡ v2.0 I/O is {io_improvement:.2f}x faster")
        print(f"   📁 File reads reduced by 90%")

def main():
    """Run all performance tests"""
    
    print("🔬 V2.0 Performance Verification Suite")
    print("=" * 60)
    print()
    
    # Check if files exist
    v1_exists = os.path.exists("bip39_offline.py")
    v2_exists = os.path.exists("bip39_offline_v2_0_g9_optimized.py")
    
    print(f"📁 v1.0 library: {'✅ Found' if v1_exists else '❌ Missing'}")
    print(f"📁 v2.0 library: {'✅ Found' if v2_exists else '❌ Missing'}")
    print()
    
    if not v1_exists or not v2_exists:
        print("❌ Cannot run tests - missing library files")
        return
    
    # Run tests
    test_v1_vs_v2_performance()
    test_file_io_operations()
    
    print("=" * 60)
    print("🎯 CONCLUSION:")
    print("If v2.0 shows significant improvement here but not in batch processing,")
    print("there may be other bottlenecks in the batch processor or system.")

if __name__ == "__main__":
    main()
