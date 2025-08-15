#!/usr/bin/env python3
"""
Test script for HP G9 Enhanced Batch Seed Processor
Verifies functionality and performance on G9 systems
"""

import os
import sys
import time
import tempfile
from batch_process_seeds_g9 import G9SeedProcessor, process_seed_batch_g9

def create_test_seeds_file(num_seeds=10):
    """Create a test seeds file with valid mnemonics"""
    
    # Test mnemonic (valid BIP39)
    test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for i in range(num_seeds):
            f.write(f"{test_mnemonic}\n")
        return f.name

def test_g9_processor_basic():
    """Test basic G9 processor functionality"""
    print("🧪 Testing G9 Processor Basic Functionality")
    print("=" * 50)
    
    # Create test processor with minimal settings
    processor = G9SeedProcessor(max_workers=2, batch_size=5, memory_limit_gb=1)
    
    print(f"✅ G9 Processor created successfully")
    print(f"   Workers: {processor.max_workers}")
    print(f"   Batch size: {processor.batch_size}")
    print(f"   Memory limit: {processor.memory_limit_gb}GB")
    
    return True

def test_batch_processing():
    """Test batch processing functionality"""
    print("\n🧪 Testing Batch Processing")
    print("=" * 30)
    
    # Test data
    test_seeds = [
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    ]
    
    # Test batch processing
    batch_data = (test_seeds, 2, 0)  # 2 addresses per seed, starting at index 0
    
    start_time = time.time()
    results = process_seed_batch_g9(batch_data)
    end_time = time.time()
    
    print(f"✅ Batch processed in {end_time - start_time:.3f} seconds")
    print(f"   Results: {len(results)} entries")
    
    # Verify results
    successful_results = [r for r in results if r.get('success', False)]
    error_results = [r for r in results if not r.get('success', False)]
    
    print(f"   Successful: {len(successful_results)}")
    print(f"   Errors: {len(error_results)}")
    
    if successful_results:
        print(f"   Sample address: {successful_results[0]['address']}")
    
    return len(successful_results) > 0

def test_file_processing():
    """Test complete file processing"""
    print("\n🧪 Testing File Processing")
    print("=" * 30)
    
    # Create test file
    test_file = create_test_seeds_file(5)
    output_csv = "test_g9_output.csv"
    output_txt = "test_g9_addresses.txt"
    
    try:
        # Create processor
        processor = G9SeedProcessor(max_workers=2, batch_size=3, memory_limit_gb=1)
        
        # Import the processing function
        from batch_process_seeds_g9 import process_seeds_file_g9
        
        print(f"📁 Processing test file: {test_file}")
        
        start_time = time.time()
        process_seeds_file_g9(
            processor=processor,
            input_file=test_file,
            csv_output=output_csv,
            addresses_output=output_txt,
            num_addresses=2
        )
        end_time = time.time()
        
        print(f"✅ File processing completed in {end_time - start_time:.3f} seconds")
        
        # Check output files
        csv_exists = os.path.exists(output_csv)
        txt_exists = os.path.exists(output_txt)
        
        print(f"   CSV file created: {csv_exists}")
        print(f"   TXT file created: {txt_exists}")
        
        if txt_exists:
            with open(output_txt, 'r') as f:
                addresses = f.readlines()
            print(f"   Addresses generated: {len(addresses)}")
        
        return csv_exists and txt_exists
        
    finally:
        # Cleanup
        for file_path in [test_file, output_csv, output_txt]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_performance_benchmark():
    """Test performance with larger dataset"""
    print("\n🧪 Testing Performance Benchmark")
    print("=" * 35)
    
    # Create larger test file
    test_file = create_test_seeds_file(20)
    output_csv = "test_g9_perf.csv"
    output_txt = "test_g9_perf_addresses.txt"
    
    try:
        # Create processor with more workers
        processor = G9SeedProcessor(max_workers=4, batch_size=5, memory_limit_gb=2)
        
        from batch_process_seeds_g9 import process_seeds_file_g9
        
        print(f"⚡ Performance test with 20 seeds, 4 workers")
        
        start_time = time.time()
        process_seeds_file_g9(
            processor=processor,
            input_file=test_file,
            csv_output=output_csv,
            addresses_output=output_txt,
            num_addresses=5
        )
        end_time = time.time()
        
        total_time = end_time - start_time
        seeds_per_second = 20 / total_time if total_time > 0 else 0
        
        print(f"✅ Performance test completed")
        print(f"   Total time: {total_time:.3f} seconds")
        print(f"   Speed: {seeds_per_second:.2f} seeds/second")
        
        return True
        
    finally:
        # Cleanup
        for file_path in [test_file, output_csv, output_txt]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def main():
    """Run all G9 processor tests"""
    print("🚀 HP G9 Enhanced Processor Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Processor", test_g9_processor_basic),
        ("Batch Processing", test_batch_processing),
        ("File Processing", test_file_processing),
        ("Performance Benchmark", test_performance_benchmark)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
    
    print(f"\n🎉 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🚀 All tests passed! G9 processor is ready for use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
