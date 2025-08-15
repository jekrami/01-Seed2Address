#!/usr/bin/env python3
"""
Performance comparison between original and G9 enhanced processors
Shows the performance improvements on HP G9 servers
"""

import time
import tempfile
import os
import psutil
from multiprocessing import cpu_count

def create_test_file(num_seeds=50):
    """Create test file with specified number of seeds"""
    test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for i in range(num_seeds):
            f.write(f"{test_mnemonic}\n")
        return f.name

def test_original_processor(test_file, num_seeds):
    """Test original sequential processor"""
    print("🔄 Testing Original Processor (Sequential)")
    print("-" * 40)
    
    try:
        from bip39_offline import process_seeds_file
        
        output_csv = "original_test.csv"
        output_txt = "original_test.txt"
        
        start_time = time.time()
        start_memory = psutil.virtual_memory().percent
        
        process_seeds_file(
            input_file=test_file,
            csv_output=output_csv,
            addresses_output=output_txt,
            num_addresses=5
        )
        
        end_time = time.time()
        end_memory = psutil.virtual_memory().percent
        
        total_time = end_time - start_time
        seeds_per_second = num_seeds / total_time if total_time > 0 else 0
        
        # Count addresses generated
        addresses_count = 0
        if os.path.exists(output_txt):
            with open(output_txt, 'r') as f:
                addresses_count = len(f.readlines())
        
        print(f"✅ Original Processing Complete")
        print(f"   Time: {total_time:.2f} seconds")
        print(f"   Speed: {seeds_per_second:.2f} seeds/second")
        print(f"   Addresses: {addresses_count}")
        print(f"   Memory usage: {start_memory:.1f}% → {end_memory:.1f}%")
        
        # Cleanup
        for file_path in [output_csv, output_txt]:
            if os.path.exists(file_path):
                os.unlink(file_path)
        
        return {
            'time': total_time,
            'speed': seeds_per_second,
            'addresses': addresses_count,
            'memory_start': start_memory,
            'memory_end': end_memory
        }
        
    except Exception as e:
        print(f"❌ Original processor error: {str(e)}")
        return None

def test_g9_processor(test_file, num_seeds):
    """Test G9 enhanced parallel processor"""
    print("\n⚡ Testing G9 Enhanced Processor (Parallel)")
    print("-" * 40)
    
    try:
        from batch_process_seeds_g9 import G9SeedProcessor, process_seeds_file_g9
        
        output_csv = "g9_test.csv"
        output_txt = "g9_test.txt"
        
        # Create G9 processor with moderate settings for testing
        cores = cpu_count()
        workers = min(8, max(2, cores // 2))  # Use reasonable number for testing
        
        processor = G9SeedProcessor(
            max_workers=workers,
            batch_size=10,
            memory_limit_gb=4
        )
        
        start_time = time.time()
        start_memory = psutil.virtual_memory().percent
        
        process_seeds_file_g9(
            processor=processor,
            input_file=test_file,
            csv_output=output_csv,
            addresses_output=output_txt,
            num_addresses=5
        )
        
        end_time = time.time()
        end_memory = psutil.virtual_memory().percent
        
        total_time = end_time - start_time
        seeds_per_second = num_seeds / total_time if total_time > 0 else 0
        
        # Count addresses generated
        addresses_count = 0
        if os.path.exists(output_txt):
            with open(output_txt, 'r') as f:
                addresses_count = len(f.readlines())
        
        print(f"✅ G9 Processing Complete")
        print(f"   Time: {total_time:.2f} seconds")
        print(f"   Speed: {seeds_per_second:.2f} seeds/second")
        print(f"   Addresses: {addresses_count}")
        print(f"   Workers used: {workers}")
        print(f"   Memory usage: {start_memory:.1f}% → {end_memory:.1f}%")
        
        # Cleanup
        for file_path in [output_csv, output_txt]:
            if os.path.exists(file_path):
                os.unlink(file_path)
        
        return {
            'time': total_time,
            'speed': seeds_per_second,
            'addresses': addresses_count,
            'workers': workers,
            'memory_start': start_memory,
            'memory_end': end_memory
        }
        
    except Exception as e:
        print(f"❌ G9 processor error: {str(e)}")
        return None

def display_comparison(original_stats, g9_stats, num_seeds):
    """Display detailed performance comparison"""
    print("\n📊 Performance Comparison Results")
    print("=" * 60)
    
    if not original_stats or not g9_stats:
        print("❌ Cannot compare - one or both tests failed")
        return
    
    # Calculate improvements
    time_improvement = ((original_stats['time'] - g9_stats['time']) / original_stats['time']) * 100
    speed_improvement = ((g9_stats['speed'] - original_stats['speed']) / original_stats['speed']) * 100
    
    print(f"🔢 Test Configuration:")
    print(f"   Seeds processed: {num_seeds}")
    print(f"   Addresses per seed: 25 (5 per derivation path)")
    print(f"   System cores: {cpu_count()}")
    print(f"   System memory: {psutil.virtual_memory().total / (1024**3):.1f}GB")
    
    print(f"\n⏱️  Processing Time:")
    print(f"   Original: {original_stats['time']:.2f} seconds")
    print(f"   G9 Enhanced: {g9_stats['time']:.2f} seconds")
    print(f"   Improvement: {time_improvement:+.1f}% {'(faster)' if time_improvement > 0 else '(slower)'}")
    
    print(f"\n🚀 Processing Speed:")
    print(f"   Original: {original_stats['speed']:.2f} seeds/second")
    print(f"   G9 Enhanced: {g9_stats['speed']:.2f} seeds/second")
    print(f"   Improvement: {speed_improvement:+.1f}% {'(faster)' if speed_improvement > 0 else '(slower)'}")
    
    print(f"\n💻 Resource Usage:")
    print(f"   Original: Sequential processing")
    print(f"   G9 Enhanced: {g9_stats['workers']} parallel workers")
    
    print(f"\n🧠 Memory Usage:")
    print(f"   Original: {original_stats['memory_start']:.1f}% → {original_stats['memory_end']:.1f}%")
    print(f"   G9 Enhanced: {g9_stats['memory_start']:.1f}% → {g9_stats['memory_end']:.1f}%")
    
    # Projected G9 performance
    print(f"\n🎯 Projected G9 Server Performance (140+ cores, 256GB RAM):")
    g9_full_workers = int(cpu_count() * 0.85) if cpu_count() > 100 else 120
    projected_speedup = g9_full_workers / g9_stats['workers']
    projected_speed = g9_stats['speed'] * projected_speedup
    
    print(f"   Estimated workers: {g9_full_workers}")
    print(f"   Projected speed: {projected_speed:.1f} seeds/second")
    print(f"   Estimated throughput: {projected_speed * 25:.0f} addresses/second")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if speed_improvement > 50:
        print("   ✅ G9 version shows excellent performance improvement")
        print("   🚀 Recommended for production use on G9 servers")
    elif speed_improvement > 0:
        print("   ✅ G9 version shows performance improvement")
        print("   📈 Consider using G9 version for better throughput")
    else:
        print("   ⚠️  G9 version may need tuning for this system")
        print("   🔧 Try adjusting worker count and batch size")

def main():
    """Run performance comparison"""
    print("🏁 HP G9 vs Original Processor Performance Comparison")
    print("=" * 70)
    
    # Test configuration
    num_seeds = 50
    print(f"🧪 Test Configuration: {num_seeds} seeds, 5 addresses per derivation path")
    print(f"💻 System: {cpu_count()} cores, {psutil.virtual_memory().total / (1024**3):.1f}GB RAM")
    
    # Create test file
    test_file = create_test_file(num_seeds)
    
    try:
        # Test original processor
        original_stats = test_original_processor(test_file, num_seeds)
        
        # Test G9 processor
        g9_stats = test_g9_processor(test_file, num_seeds)
        
        # Display comparison
        display_comparison(original_stats, g9_stats, num_seeds)
        
    finally:
        # Cleanup test file
        if os.path.exists(test_file):
            os.unlink(test_file)
    
    print(f"\n🎉 Performance comparison complete!")

if __name__ == "__main__":
    main()
