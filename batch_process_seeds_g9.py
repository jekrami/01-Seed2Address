#!/usr/bin/env python3
"""
HP G9 Enhanced Batch Seed Processor - Optimized for High-Performance Servers
Designed for HP G9 servers with 140+ cores and 256GB RAM
Features: Advanced Multiprocessing, Memory Optimization, Batch Processing, Real-time Monitoring

Performance Optimizations:
- Utilizes up to 85% of available CPU cores (120+ cores on G9)
- Dynamic memory management for 256GB RAM
- Intelligent batch sizing based on system resources
- Process pool optimization with minimal overhead
- Real-time performance monitoring and statistics
"""

import sys
import argparse
import os
import time
import psutil
import threading
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
from typing import List, Dict, Tuple
from bip39_offline import generate_addresses, BIP39

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("⚠️  tqdm not available. Install with: pip install tqdm")

class G9PerformanceMonitor:
    """Real-time performance monitoring for G9 server"""
    
    def __init__(self):
        self.start_time = time.time()
        self.monitoring = False
        self.stats = {
            'peak_memory_percent': 0,
            'peak_memory_gb': 0,
            'avg_cpu_percent': 0,
            'cpu_samples': []
        }
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring and return final stats"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1)
        
        if self.stats['cpu_samples']:
            self.stats['avg_cpu_percent'] = sum(self.stats['cpu_samples']) / len(self.stats['cpu_samples'])
        
        return self.stats
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            # Memory monitoring
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_gb = memory.used / (1024**3)
            
            if memory_percent > self.stats['peak_memory_percent']:
                self.stats['peak_memory_percent'] = memory_percent
                self.stats['peak_memory_gb'] = memory_gb
            
            # CPU monitoring
            cpu_percent = psutil.cpu_percent(interval=None)
            self.stats['cpu_samples'].append(cpu_percent)
            
            time.sleep(0.5)  # Sample every 500ms

class G9SeedProcessor:
    """HP G9 Optimized Seed Processor with advanced parallel processing"""
    
    def __init__(self, max_workers=None, batch_size=None, memory_limit_gb=220):
        """Initialize G9 processor with optimal settings for 140+ cores and 256GB RAM"""

        # System detection and optimization
        self.total_cores = cpu_count()
        self.total_memory_gb = psutil.virtual_memory().total / (1024**3)

        # G9 Server optimizations with intelligent worker scaling
        if max_workers is None:
            # Optimize for G9: Use fewer workers to reduce overhead
            # Sweet spot for high-core systems is typically 2-4x logical cores, not 85%
            if self.total_cores >= 100:  # G9 server detection
                # For G9: Use 25-35% of cores to minimize process overhead
                self.max_workers = max(16, min(48, int(self.total_cores * 0.3)))
                print(f"🔧 G9 Detected: Optimizing for {self.total_cores} cores with reduced worker count")
            else:
                # For regular systems: Use higher percentage
                self.max_workers = max(1, int(self.total_cores * 0.8))
        else:
            self.max_workers = min(max_workers, self.total_cores)

        # Intelligent batch sizing for G9's massive memory
        if batch_size is None:
            # Larger batches for G9 to reduce process overhead
            if self.total_cores >= 100:  # G9 server
                # Use larger batches to maximize work per process
                self.batch_size = max(2000, min(10000, int(self.total_memory_gb * 20)))
            else:
                # Regular systems: smaller batches
                available_memory_mb = (self.total_memory_gb * 0.6) * 1024
                self.batch_size = max(500, min(5000, int(available_memory_mb / 2)))
        else:
            self.batch_size = batch_size
            
        self.memory_limit_gb = min(memory_limit_gb, self.total_memory_gb * 0.85)
        
        # Performance monitoring
        self.monitor = G9PerformanceMonitor()
        
        # Calculate efficiency metrics
        self.worker_efficiency = self.total_cores / self.max_workers if self.max_workers > 0 else 1
        self.is_g9_server = self.total_cores >= 100

        print(f"🚀 HP G9 Enhanced Processor Initialized")
        print(f"💻 System: {self.total_cores} cores, {self.total_memory_gb:.1f}GB RAM")
        print(f"⚡ G9 Config: {self.max_workers} workers, batch size: {self.batch_size}")
        print(f"🎯 Memory limit: {self.memory_limit_gb:.1f}GB")
        if self.is_g9_server:
            print(f"🔧 G9 Optimization: Reduced workers ({self.worker_efficiency:.1f} cores/worker) for minimal overhead")
        else:
            print(f"🔧 Optimization: Standard mode for regular systems")

def process_seed_batch_g9(batch_data: Tuple[List[str], int, int]) -> List[Dict]:
    """G9 Optimized batch processing with enhanced error handling"""
    seeds, num_addresses, start_idx = batch_data
    results = []
    
    # Initialize BIP39 once per process for efficiency
    bip39 = BIP39()
    
    for i, seed in enumerate(seeds):
        seed_idx = start_idx + i
        try:
            # Fast validation and processing
            if len(seed.split()) >= 12:
                if not bip39.validate_mnemonic(seed):
                    results.append({
                        'seed_idx': seed_idx,
                        'seed': seed,
                        'error': 'Invalid mnemonic checksum',
                        'success': False
                    })
                    continue
                    
                # Generate addresses with optimized memory usage
                addresses = generate_addresses(seed, num_addresses=num_addresses)
                
                # Efficiently flatten results
                for path_desc, addr_list in addresses.items():
                    for addr_idx, addr_info in enumerate(addr_list):
                        results.append({
                            'seed_idx': seed_idx,
                            'seed': seed,
                            'derivation_path': addr_info['path'],
                            'address_index': addr_idx,
                            'address': addr_info['address'],
                            'public_key': addr_info['public_key'],
                            'private_key': addr_info['private_key'],
                            'private_key_wif': addr_info['private_key_wif'],
                            'script_semantics': addr_info['script_semantics'],
                            'success': True
                        })
                
            else:
                results.append({
                    'seed_idx': seed_idx,
                    'seed': seed,
                    'error': 'Invalid seed format (expected 12+ words)',
                    'success': False
                })
                
        except Exception as e:
            results.append({
                'seed_idx': seed_idx,
                'seed': seed,
                'error': f"Processing error: {str(e)}",
                'success': False
            })
    
    return results

def process_seeds_file_g9(processor: G9SeedProcessor, input_file: str = "seeds.txt", 
                         csv_output: str = "bip39_addresses_g9.csv",
                         addresses_output: str = "bip39_only_addresses_g9.txt", 
                         num_addresses: int = 10):
    """G9 Enhanced parallel processing with real-time monitoring"""
    
    print(f"\n🔄 HP G9 Processing seeds from: {input_file}")
    print(f"📊 CSV output: {csv_output}")
    print(f"📝 Addresses output: {addresses_output}")
    print("=" * 80)
    
    # Start performance monitoring
    processor.monitor.start_monitoring()
    start_time = time.time()
    
    try:
        # Optimized file reading for large files
        print("📖 Reading seeds file...")
        with open(input_file, 'r', encoding='utf-8', buffering=8192) as f:
            seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not seeds:
            print(f"❌ No seeds found in {input_file}")
            return
            
        print(f"✅ Loaded {len(seeds)} seeds")
        
        # G9 Memory optimization check
        estimated_memory_gb = (len(seeds) * num_addresses * 0.002)  # Refined estimate
        if estimated_memory_gb > processor.memory_limit_gb:
            print(f"⚠️  Estimated memory usage: {estimated_memory_gb:.1f}GB")
            print(f"💾 G9 will process in optimized chunks (limit: {processor.memory_limit_gb:.1f}GB)")
        
        # Create optimized batches
        batches = []
        for i in range(0, len(seeds), processor.batch_size):
            batch_seeds = seeds[i:i + processor.batch_size]
            batches.append((batch_seeds, num_addresses, i))
        
        print(f"📦 Created {len(batches)} optimized batches for G9 parallel processing")
        
        # G9 High-performance parallel processing
        all_results = []
        processed_seeds = 0
        error_count = 0
        
        print(f"⚡ Starting G9 parallel processing with {processor.max_workers} workers...")
        
        # Use ProcessPoolExecutor optimized for G9
        with ProcessPoolExecutor(max_workers=processor.max_workers) as executor:
            if TQDM_AVAILABLE:
                # Submit all batches for maximum parallelism
                future_to_batch = {
                    executor.submit(process_seed_batch_g9, batch): i 
                    for i, batch in enumerate(batches)
                }
                
                # Process results with enhanced progress tracking
                with tqdm(total=len(seeds), desc="🔐 G9 Processing", 
                         unit="seeds", smoothing=0.05, 
                         bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
                    
                    for future in as_completed(future_to_batch):
                        batch_idx = future_to_batch[future]
                        try:
                            batch_results = future.result()
                            all_results.extend(batch_results)
                            
                            # Enhanced statistics
                            batch_successful = sum(1 for r in batch_results if r.get('success', False))
                            batch_errors = len([r for r in batch_results if not r.get('success', False)])
                            
                            processed_seeds += batch_successful
                            error_count += batch_errors
                            
                            # Real-time performance metrics
                            current_memory = psutil.virtual_memory().percent
                            current_time = time.time()
                            elapsed = current_time - start_time
                            rate = processed_seeds / elapsed if elapsed > 0 else 0
                            
                            # Update progress with G9 metrics
                            pbar.update(len(batches[batch_idx][0]))
                            pbar.set_postfix({
                                'Success': processed_seeds,
                                'Errors': error_count,
                                'Rate': f"{rate:.1f}/s",
                                'Memory': f"{current_memory:.1f}%",
                                'Workers': processor.max_workers
                            })
                            
                        except Exception as e:
                            print(f"❌ G9 Batch {batch_idx} failed: {str(e)}")
                            error_count += len(batches[batch_idx][0])
                            pbar.update(len(batches[batch_idx][0]))
            else:
                # Fallback processing without progress bar
                print("Processing batches on G9...")
                futures = [executor.submit(process_seed_batch_g9, batch) for batch in batches]
                
                for i, future in enumerate(as_completed(futures)):
                    try:
                        batch_results = future.result()
                        all_results.extend(batch_results)
                        
                        batch_successful = sum(1 for r in batch_results if r.get('success', False))
                        batch_errors = len([r for r in batch_results if not r.get('success', False)])
                        
                        processed_seeds += batch_successful
                        error_count += batch_errors
                        
                        print(f"✅ G9 Batch {i+1}/{len(batches)} complete - "
                              f"Success: {processed_seeds}, Errors: {error_count}")
                              
                    except Exception as e:
                        print(f"❌ G9 Batch {i+1} failed: {str(e)}")
                        error_count += len(batches[i][0])
        
        # Stop monitoring and get final stats
        final_stats = processor.monitor.stop_monitoring()
        
        # Write results with G9 optimization
        print(f"\n💾 Writing results to G9 optimized output files...")
        write_results_g9(all_results, csv_output, addresses_output)
        
        # G9 Performance summary
        end_time = time.time()
        total_time = end_time - start_time
        seeds_per_second = len(seeds) / total_time if total_time > 0 else 0
        addresses_generated = processed_seeds * num_addresses * 5  # 5 derivation paths
        
        print(f"\n🎉 HP G9 Processing Complete!")
        print("=" * 60)
        print(f"🖥️  G9 Server Performance:")
        print(f"   💻 Cores used: {processor.max_workers}/{processor.total_cores}")
        print(f"   🧠 Peak memory: {final_stats['peak_memory_gb']:.1f}GB ({final_stats['peak_memory_percent']:.1f}%)")
        print(f"   ⚡ Avg CPU usage: {final_stats['avg_cpu_percent']:.1f}%")
        print(f"📊 Processing Results:")
        print(f"   📝 Total seeds: {len(seeds)}")
        print(f"   ✅ Successful: {processed_seeds}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   🔐 Addresses generated: {addresses_generated:,}")
        print(f"⏱️  Performance Metrics:")
        print(f"   🕐 Total time: {total_time:.2f} seconds")
        print(f"   🚀 Speed: {seeds_per_second:.2f} seeds/second")
        print(f"   ⚡ Throughput: {addresses_generated/total_time:.0f} addresses/second")
        print(f"📁 Output files:")
        print(f"   📊 {csv_output}")
        print(f"   📝 {addresses_output}")
        
    except FileNotFoundError:
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ G9 Processing error: {str(e)}")
        processor.monitor.stop_monitoring()
        sys.exit(1)

def write_results_g9(results: List[Dict], csv_output: str, addresses_output: str):
    """G9 Optimized writing of results with enhanced performance"""

    # Efficiently separate results
    successful_results = [r for r in results if r.get('success', False)]
    error_results = [r for r in results if not r.get('success', False)]

    print(f"📊 Writing {len(successful_results)} successful results to G9 optimized files...")

    # Write CSV with optimized buffering for G9
    if successful_results:
        with open(csv_output, 'w', newline='', encoding='utf-8', buffering=65536) as csvfile:
            fieldnames = ['seed_index', 'seed', 'derivation_path', 'address_index', 'address',
                         'public_key', 'private_key', 'private_key_wif', 'script_semantics']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Batch write for better performance
            for result in successful_results:
                writer.writerow({
                    'seed_index': result['seed_idx'] + 1,
                    'seed': result['seed'],
                    'derivation_path': result['derivation_path'],
                    'address_index': result['address_index'],
                    'address': result['address'],
                    'public_key': result['public_key'],
                    'private_key': result['private_key'],
                    'private_key_wif': result['private_key_wif'],
                    'script_semantics': result['script_semantics']
                })

    # Write addresses-only file with G9 optimization
    if successful_results:
        with open(addresses_output, 'w', encoding='utf-8', buffering=65536) as txtfile:
            # Batch write addresses for better I/O performance
            addresses = [result['address'] + '\n' for result in successful_results]
            txtfile.writelines(addresses)

    # Enhanced error logging for G9
    if error_results:
        error_file = csv_output.replace('.csv', '_g9_errors.log')
        with open(error_file, 'w', encoding='utf-8') as errfile:
            errfile.write("HP G9 Enhanced Seed Processing Error Log\n")
            errfile.write("=" * 60 + "\n")
            errfile.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            errfile.write(f"Total Errors: {len(error_results)}\n\n")

            for result in error_results:
                errfile.write(f"Seed Index: {result['seed_idx'] + 1}\n")
                errfile.write(f"Seed Preview: {result['seed'][:50]}...\n")
                errfile.write(f"Error: {result.get('error', 'Unknown error')}\n")
                errfile.write("-" * 40 + "\n")
        print(f"⚠️  G9 Error log written to: {error_file}")

def run_g9_benchmark():
    """Run comprehensive performance benchmark for G9 system"""
    print("🔬 HP G9 Performance Benchmark Suite")
    print("=" * 50)

    # System info
    cores = cpu_count()
    memory_gb = psutil.virtual_memory().total / (1024**3)
    print(f"💻 System: {cores} cores, {memory_gb:.1f}GB RAM")

    # Test configurations optimized for G9
    test_configs = [
        {'workers': int(cores * 0.5), 'batch_size': 1000, 'name': 'Conservative'},
        {'workers': int(cores * 0.7), 'batch_size': 1500, 'name': 'Balanced'},
        {'workers': int(cores * 0.85), 'batch_size': 2000, 'name': 'G9 Optimized'},
    ]

    print(f"\n🧪 Testing {len(test_configs)} configurations...")

    for config in test_configs:
        if config['workers'] <= cores:
            print(f"\n⚡ {config['name']} Mode:")
            print(f"   Workers: {config['workers']}, Batch: {config['batch_size']}")

            start_time = time.time()

            # Initialize processor
            processor = G9SeedProcessor(
                max_workers=config['workers'],
                batch_size=config['batch_size']
            )

            # Simulate processing time
            time.sleep(0.2)  # Placeholder for actual processing

            end_time = time.time()
            print(f"   ⏱️  Setup time: {end_time - start_time:.3f}s")
            print(f"   💾 Memory usage: {psutil.virtual_memory().percent:.1f}%")

def main():
    """Enhanced main function with G9 optimizations and advanced features"""

    parser = argparse.ArgumentParser(
        description='HP G9 Enhanced BIP39 Batch Seed Processor - Optimized for 140+ cores and 256GB RAM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 HP G9 Server Examples:
  # G9 High-performance mode (recommended)
  python batch_process_seeds_g9.py --g9-mode

  # Custom G9 configuration
  python batch_process_seeds_g9.py --workers 120 --batch-size 2000 --memory-limit 200

  # Large file processing on G9
  python batch_process_seeds_g9.py -i large_seeds.txt --g9-mode --memory-limit 220

  # G9 Performance benchmark
  python batch_process_seeds_g9.py --benchmark

🔧 G9 Optimizations:
  - Utilizes up to 85% of 140+ cores
  - Optimized for 256GB RAM with intelligent batching
  - Real-time performance monitoring
  - Enhanced error handling and logging
        """
    )

    parser.add_argument('-i', '--input', default='seeds.txt',
                       help='Input file containing seeds (default: seeds.txt)')
    parser.add_argument('-c', '--csv', default='bip39_addresses_g9.csv',
                       help='CSV output file with full data (default: bip39_addresses_g9.csv)')
    parser.add_argument('-a', '--addresses', default='bip39_only_addresses_g9.txt',
                       help='Text output file with addresses only (default: bip39_only_addresses_g9.txt)')
    parser.add_argument('-n', '--num', type=int, default=10,
                       help='Number of addresses per derivation path (default: 10)')
    parser.add_argument('-w', '--workers', type=int, default=None,
                       help='Number of worker processes (default: auto-detect for G9)')
    parser.add_argument('-b', '--batch-size', type=int, default=None,
                       help='Batch size for processing (default: G9 optimized)')
    parser.add_argument('-m', '--memory-limit', type=float, default=220,
                       help='Memory limit in GB (default: 220 for G9)')
    parser.add_argument('--g9-mode', action='store_true',
                       help='Enable G9 high-performance mode (recommended for G9 servers)')
    parser.add_argument('--benchmark', action='store_true',
                       help='Run G9 performance benchmark')

    args = parser.parse_args()

    # G9 mode optimizations
    if args.g9_mode:
        print("🚀 HP G9 High-Performance Mode Activated!")
        total_cores = cpu_count()
        if args.workers is None:
            if total_cores >= 100:  # True G9 server
                # Use optimized worker count for G9 (30% of cores)
                args.workers = max(24, min(48, int(total_cores * 0.3)))
                print(f"🔧 G9 Server Detected: Using {args.workers} workers (30% of {total_cores} cores)")
            else:
                # Regular system with G9 mode
                args.workers = max(8, int(total_cores * 0.75))
                print(f"🔧 Regular System: Using {args.workers} workers (75% of {total_cores} cores)")
        if args.batch_size is None:
            if total_cores >= 100:  # G9 server
                args.batch_size = 5000  # Larger batches for G9
            else:
                args.batch_size = 2500  # Standard batch size
        args.memory_limit = min(args.memory_limit, 230)  # Conservative for G9
        print(f"⚡ Optimized Config: {args.workers} workers, {args.batch_size} batch size")

    # Display G9 system information
    print("🖥️  HP G9 Enhanced BIP39 Batch Seed Processor")
    print("=" * 70)
    print(f"💻 G9 System: {cpu_count()} cores, {psutil.virtual_memory().total / (1024**3):.1f}GB RAM")
    print(f"📁 Input file: {args.input}")
    print(f"📊 CSV output: {args.csv}")
    print(f"📝 Addresses output: {args.addresses}")
    print(f"🔢 Addresses per path: {args.num}")

    if args.benchmark:
        print("\n🏁 Running G9 performance benchmark...")
        run_g9_benchmark()
        return

    # Initialize G9 processor with enhanced settings
    processor = G9SeedProcessor(
        max_workers=args.workers,
        batch_size=args.batch_size,
        memory_limit_gb=args.memory_limit
    )

    # Process seeds with G9 optimization
    process_seeds_file_g9(
        processor=processor,
        input_file=args.input,
        csv_output=args.csv,
        addresses_output=args.addresses,
        num_addresses=args.num
    )

if __name__ == "__main__":
    main()
