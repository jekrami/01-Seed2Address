#!/usr/bin/env python3
"""
G9 Performance Tuner - Find optimal settings for your G9 server
This script tests different worker and batch size combinations to find the sweet spot
"""

import time
import psutil
from multiprocessing import cpu_count
import subprocess
import sys
import os

def run_performance_test(workers, batch_size, test_seeds=100):
    """Run a performance test with specific settings"""
    
    # Create a small test file
    test_file = "g9_perf_test_seeds.txt"
    
    # Use first few lines from the main seeds file
    try:
        with open("d:\\Work.AUG\\seeds_20250812_143051.txt", 'r') as f:
            seeds = [line.strip() for line in f if line.strip()][:test_seeds]
        
        with open(test_file, 'w') as f:
            for seed in seeds:
                f.write(seed + '\n')
    except FileNotFoundError:
        print("❌ Main seeds file not found. Creating dummy test data...")
        # Create dummy test data
        dummy_seeds = [
            "motor venture dilemma quote subject magnet keep large dry gossip bean paper",
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "legal winner thank year wave sausage worth useful legal winner thank yellow"
        ] * (test_seeds // 3 + 1)
        
        with open(test_file, 'w') as f:
            for seed in dummy_seeds[:test_seeds]:
                f.write(seed + '\n')
    
    # Run the test
    cmd = [
        sys.executable, "batch_process_seeds_g9.py",
        "-i", test_file,
        "-c", f"perf_test_{workers}w_{batch_size}b.csv",
        "-a", f"perf_test_{workers}w_{batch_size}b.txt",
        "-w", str(workers),
        "-b", str(batch_size),
        "-n", "2"  # Only 2 addresses per path for speed
    ]
    
    print(f"🧪 Testing: {workers} workers, batch size {batch_size}")
    
    start_time = time.time()
    start_memory = psutil.virtual_memory().percent
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        end_time = time.time()
        end_memory = psutil.virtual_memory().percent
        
        if result.returncode == 0:
            # Extract performance metrics from output
            output_lines = result.stdout.split('\n')
            total_time = end_time - start_time
            
            # Look for speed in output
            speed = 0
            for line in output_lines:
                if "🚀 Speed:" in line:
                    try:
                        speed = float(line.split("🚀 Speed:")[1].split("seeds/second")[0].strip())
                    except:
                        pass
            
            if speed == 0:
                speed = test_seeds / total_time if total_time > 0 else 0
            
            return {
                'workers': workers,
                'batch_size': batch_size,
                'total_time': total_time,
                'speed': speed,
                'memory_delta': end_memory - start_memory,
                'success': True,
                'error': None
            }
        else:
            return {
                'workers': workers,
                'batch_size': batch_size,
                'total_time': end_time - start_time,
                'speed': 0,
                'memory_delta': 0,
                'success': False,
                'error': result.stderr[:200] if result.stderr else "Unknown error"
            }
    
    except subprocess.TimeoutExpired:
        return {
            'workers': workers,
            'batch_size': batch_size,
            'total_time': 120,
            'speed': 0,
            'memory_delta': 0,
            'success': False,
            'error': "Timeout (>120s)"
        }
    except Exception as e:
        return {
            'workers': workers,
            'batch_size': batch_size,
            'total_time': 0,
            'speed': 0,
            'memory_delta': 0,
            'success': False,
            'error': str(e)[:200]
        }
    finally:
        # Cleanup
        for ext in ['.csv', '.txt']:
            try:
                os.remove(f"perf_test_{workers}w_{batch_size}b{ext}")
            except:
                pass
        try:
            os.remove(test_file)
        except:
            pass

def main():
    """Run G9 performance tuning tests"""
    
    print("🔬 G9 Performance Tuner")
    print("=" * 60)
    
    cores = cpu_count()
    memory_gb = psutil.virtual_memory().total / (1024**3)
    
    print(f"💻 System: {cores} cores, {memory_gb:.1f}GB RAM")
    
    if cores < 100:
        print("⚠️  This doesn't appear to be a G9 server (expected 140+ cores)")
        print("   Running tests anyway for comparison...")
    
    print("\n🧪 Testing different configurations...")
    print("   This will take several minutes...")
    
    # Test configurations
    if cores >= 100:  # G9 server
        test_configs = [
            # Low worker count (recommended for G9)
            {'workers': 16, 'batch_size': 2000},
            {'workers': 24, 'batch_size': 3000},
            {'workers': 32, 'batch_size': 4000},
            {'workers': 40, 'batch_size': 5000},
            {'workers': 48, 'batch_size': 6000},
            
            # Medium worker count
            {'workers': 64, 'batch_size': 3000},
            {'workers': 80, 'batch_size': 2000},
            
            # High worker count (current approach)
            {'workers': int(cores * 0.85), 'batch_size': 1000},
            {'workers': int(cores * 0.85), 'batch_size': 2000},
        ]
    else:  # Regular system
        test_configs = [
            {'workers': 4, 'batch_size': 1000},
            {'workers': 8, 'batch_size': 1500},
            {'workers': int(cores * 0.5), 'batch_size': 2000},
            {'workers': int(cores * 0.75), 'batch_size': 1500},
            {'workers': int(cores * 0.85), 'batch_size': 1000},
        ]
    
    results = []
    
    for i, config in enumerate(test_configs):
        print(f"\n📊 Test {i+1}/{len(test_configs)}")
        result = run_performance_test(config['workers'], config['batch_size'])
        results.append(result)
        
        if result['success']:
            print(f"   ✅ Speed: {result['speed']:.2f} seeds/s, Time: {result['total_time']:.2f}s")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    # Analyze results
    print("\n" + "=" * 80)
    print("📈 PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    successful_results = [r for r in results if r['success']]
    
    if not successful_results:
        print("❌ No successful tests! Check your setup.")
        return
    
    # Sort by speed
    successful_results.sort(key=lambda x: x['speed'], reverse=True)
    
    print(f"{'Rank':<4} | {'Workers':<8} | {'Batch':<8} | {'Speed':<12} | {'Time':<8} | {'Memory':<8}")
    print("-" * 70)
    
    for i, result in enumerate(successful_results[:5]):
        print(f"{i+1:<4} | {result['workers']:<8} | {result['batch_size']:<8} | "
              f"{result['speed']:.2f} s/s{'':<4} | {result['total_time']:.2f}s{'':<2} | "
              f"{result['memory_delta']:+.1f}%{'':<3}")
    
    # Recommendations
    best = successful_results[0]
    print(f"\n🏆 BEST CONFIGURATION:")
    print(f"   Workers: {best['workers']}")
    print(f"   Batch Size: {best['batch_size']}")
    print(f"   Speed: {best['speed']:.2f} seeds/second")
    
    print(f"\n🚀 RECOMMENDED COMMAND:")
    print(f"   python batch_process_seeds_g9.py -w {best['workers']} -b {best['batch_size']} --g9-mode")
    
    # Analysis
    if cores >= 100:
        low_worker_results = [r for r in successful_results if r['workers'] <= 50]
        high_worker_results = [r for r in successful_results if r['workers'] > 80]
        
        if low_worker_results and high_worker_results:
            avg_low = sum(r['speed'] for r in low_worker_results) / len(low_worker_results)
            avg_high = sum(r['speed'] for r in high_worker_results) / len(high_worker_results)
            
            print(f"\n📊 G9 ANALYSIS:")
            print(f"   Low workers (≤50): {avg_low:.2f} seeds/s average")
            print(f"   High workers (>80): {avg_high:.2f} seeds/s average")
            
            if avg_low > avg_high:
                improvement = ((avg_low - avg_high) / avg_high) * 100
                print(f"   💡 Low worker count is {improvement:.1f}% faster!")
                print(f"   🔧 Recommendation: Use fewer workers to reduce process overhead")

if __name__ == "__main__":
    main()
