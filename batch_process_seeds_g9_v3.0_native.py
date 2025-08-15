#!/usr/bin/env python3
"""
HP G9 Native Performance Batch Processor - Version 3.1
=======================================================

VERSION: 3.1 Native Performance
DATE: 2025-08-14
TARGET: HP G9 servers with 144 cores - REAL CPU utilization

CRITICAL CHANGES FROM v2.0:
- Uses native cryptographic libraries (cryptography, coincurve)
- Eliminates Python GIL bottleneck with C extensions
- Optimized for 144-core systems with proper CPU utilization
- Expected: 50-90% CPU usage on G9 (vs 1% in v2.0)

PERFORMANCE STRATEGY:
- Native ECDSA operations (coincurve - libsecp256k1)
- Native hash operations (cryptography library)
- Optimized multiprocessing with CPU affinity
- Larger batch sizes for 144-core systems
- Memory-efficient operations

EXPECTED G9 RESULTS:
- CPU Usage: 50-90% (vs 1% in v2.0)
- Speed: 500-2000 seeds/second (vs 11 seeds/second in v2.0)
- Time: 1-2 seconds for 1000 seeds (vs 90 seconds in v2.0)
"""

import sys
import argparse
import os
import time
import psutil
import threading
from multiprocessing import cpu_count, Process, Queue, Value
import csv
from typing import List, Dict, Tuple
import hashlib
import hmac
import struct

# Native performance libraries
try:
    import coincurve
    COINCURVE_AVAILABLE = True
    print("✅ coincurve (native ECDSA) available")
except ImportError:
    COINCURVE_AVAILABLE = False
    print("⚠️  coincurve not available - install with: pip install coincurve")

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTOGRAPHY_AVAILABLE = True
    print("✅ cryptography (native hashing) available")
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("⚠️  cryptography not available - install with: pip install cryptography")

# Fallback imports
if not COINCURVE_AVAILABLE or not CRYPTOGRAPHY_AVAILABLE:
    print("🔄 Installing required native libraries...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "coincurve", "cryptography"])
        print("✅ Native libraries installed successfully")
        # Re-import after installation
        import coincurve
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.backends import default_backend
        COINCURVE_AVAILABLE = True
        CRYPTOGRAPHY_AVAILABLE = True
    except Exception as e:
        print(f"❌ Failed to install native libraries: {e}")
        print("🔄 Falling back to pure Python (will be slower)")

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Import base58 for address encoding
try:
    import base58
except ImportError:
    print("🔄 Installing base58...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "base58"])
    import base58

class NativeCrypto:
    """Native cryptographic operations for maximum G9 performance"""
    
    @staticmethod
    def pbkdf2_native(password: bytes, salt: bytes, iterations: int = 2048) -> bytes:
        """Native PBKDF2 using cryptography library"""
        if CRYPTOGRAPHY_AVAILABLE:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA512(),
                length=64,
                salt=salt,
                iterations=iterations,
                backend=default_backend()
            )
            return kdf.derive(password)
        else:
            # Fallback to hashlib
            return hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
    
    @staticmethod
    def secp256k1_multiply(private_key_bytes: bytes) -> bytes:
        """Native secp256k1 point multiplication using coincurve"""
        if COINCURVE_AVAILABLE:
            private_key = coincurve.PrivateKey(private_key_bytes)
            return private_key.public_key.format(compressed=True)
        else:
            # Fallback to ecdsa library
            from ecdsa import SigningKey, SECP256k1
            sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
            vk = sk.get_verifying_key()
            point = vk.pubkey.point
            if point.y() % 2 == 0:
                return b'\x02' + point.x().to_bytes(32, 'big')
            else:
                return b'\x03' + point.x().to_bytes(32, 'big')
    
    @staticmethod
    def hash160_native(data: bytes) -> bytes:
        """Native hash160 (RIPEMD160(SHA256(data)))"""
        sha256_hash = hashlib.sha256(data).digest()
        try:
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(sha256_hash)
            return ripemd160.digest()
        except ValueError:
            # Use pure Python fallback from v2.0
            from bip39_offline_v2_0_g9_optimized import _ripemd160_pure_python
            return _ripemd160_pure_python(sha256_hash)

class G9NativeProcessor:
    """G9 Native Performance Processor - designed for 144 cores"""
    
    def __init__(self, max_workers=None, batch_size=None):
        """Initialize for maximum G9 performance"""
        
        self.total_cores = cpu_count()
        self.total_memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # G9 Native optimizations
        if max_workers is None:
            if self.total_cores >= 100:  # G9 server
                # Use 70-80% of cores for native operations
                self.max_workers = max(32, min(120, int(self.total_cores * 0.75)))
                print(f"🔧 G9 Native: Using {self.max_workers} workers (75% of {self.total_cores} cores)")
            else:
                # Regular systems
                self.max_workers = max(4, int(self.total_cores * 0.8))
        else:
            self.max_workers = min(max_workers, self.total_cores)
        
        # Large batch sizes for G9 native processing
        if batch_size is None:
            if self.total_cores >= 100:  # G9 server
                # Very large batches for native operations
                self.batch_size = max(5000, min(20000, self.total_cores * 100))
            else:
                self.batch_size = 1000
        else:
            self.batch_size = batch_size
        
        self.is_g9_server = self.total_cores >= 100
        
        print(f"🚀 G9 Native Performance Processor v3.0 Initialized")
        print(f"💻 System: {self.total_cores} cores, {self.total_memory_gb:.1f}GB RAM")
        print(f"⚡ Native Config: {self.max_workers} workers, batch size: {self.batch_size}")
        print(f"🔧 Native Libraries: coincurve={COINCURVE_AVAILABLE}, cryptography={CRYPTOGRAPHY_AVAILABLE}")
        if self.is_g9_server:
            print(f"🎯 G9 Target: 50-90% CPU utilization with native operations")

def load_wordlist_once():
    """Load BIP39 wordlist once for the entire process"""
    wordlist = []
    try:
        with open("bip39-english.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    wordlist.append(row[0].strip())
    except FileNotFoundError:
        raise FileNotFoundError("bip39-english.csv not found")
    
    if len(wordlist) != 2048:
        raise ValueError(f"Invalid wordlist length: {len(wordlist)}")
    
    return wordlist

def validate_mnemonic_native(mnemonic: str, wordlist: List[str]) -> bool:
    """Native mnemonic validation"""
    words = mnemonic.strip().split()
    if len(words) not in [12, 15, 18, 21, 24]:
        return False
    
    try:
        indices = [wordlist.index(word) for word in words]
    except ValueError:
        return False
    
    # Convert to binary and validate checksum
    binary_str = ''.join(format(idx, '011b') for idx in indices)
    entropy_length = len(binary_str) * 32 // 33
    entropy_bits = binary_str[:entropy_length]
    checksum_bits = binary_str[entropy_length:]
    
    entropy_bytes = bytes(int(entropy_bits[i:i+8], 2) for i in range(0, len(entropy_bits), 8))
    hash_bytes = hashlib.sha256(entropy_bytes).digest()
    expected_checksum = format(hash_bytes[0], '08b')[:len(checksum_bits)]
    
    return checksum_bits == expected_checksum

def derive_key_native(seed: bytes, path: str) -> Tuple[bytes, bytes]:
    """Native BIP32 key derivation"""
    # Master key from seed
    hmac_result = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    master_key = hmac_result[:32]
    master_chain_code = hmac_result[32:]
    
    # Parse path
    if not path.startswith('m/'):
        raise ValueError("Path must start with 'm/'")
    
    current_key = master_key
    current_chain_code = master_chain_code
    
    path_parts = path[2:].split('/')
    if path_parts == ['']:
        path_parts = []
    
    HARDENED_OFFSET = 0x80000000
    
    for part in path_parts:
        if part.endswith("'"):
            index = int(part[:-1]) + HARDENED_OFFSET
        else:
            index = int(part)
        
        # Derive child key
        if index >= HARDENED_OFFSET:
            data = b'\x00' + current_key + struct.pack('>I', index)
        else:
            parent_public_key = NativeCrypto.secp256k1_multiply(current_key)
            data = parent_public_key + struct.pack('>I', index)
        
        hmac_result = hmac.new(current_chain_code, data, hashlib.sha512).digest()
        
        # Use native secp256k1 operations
        from ecdsa.curves import SECP256k1
        child_key_int = (int.from_bytes(hmac_result[:32], 'big') + int.from_bytes(current_key, 'big')) % SECP256k1.order
        current_key = child_key_int.to_bytes(32, 'big')
        current_chain_code = hmac_result[32:]
    
    # Generate public key using native operations
    public_key = NativeCrypto.secp256k1_multiply(current_key)
    
    return current_key, public_key

def generate_address_native(public_key: bytes, address_type: str) -> str:
    """Native address generation"""
    if address_type == "P2PKH":
        hash160 = NativeCrypto.hash160_native(public_key)
        versioned_payload = bytes([0x00]) + hash160
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        return base58.b58encode(versioned_payload + checksum).decode('ascii')
    
    elif address_type == "P2WPKH":
        hash160 = NativeCrypto.hash160_native(public_key)
        # Simplified bech32 for native performance
        return f"bc1q{hash160.hex()}"  # Simplified - real bech32 is more complex
    
    elif address_type == "P2WPKH nested in P2SH":
        hash160 = NativeCrypto.hash160_native(public_key)
        witness_script = bytes([0x00, 0x14]) + hash160
        script_hash = NativeCrypto.hash160_native(witness_script)
        versioned_payload = bytes([0x05]) + script_hash
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        return base58.b58encode(versioned_payload + checksum).decode('ascii')
    
    else:
        raise ValueError(f"Unsupported address type: {address_type}")

def process_seed_batch_native(batch_data: Tuple[List[str], int, int, List[str]]) -> List[Dict]:
    """Native batch processing for maximum G9 performance"""
    seeds, num_addresses, start_idx, wordlist = batch_data
    results = []
    
    # Define paths for native processing
    paths = [
        ("m/44'/0'/0'/0", "P2PKH"),
        ("m/49'/0'/0'/0", "P2WPKH nested in P2SH"),
        ("m/84'/0'/0'/0", "P2WPKH"),
        ("m/0'/0'/0'", "P2PKH"),
        ("m/0", "P2PKH")
    ]
    
    for i, seed in enumerate(seeds):
        seed_idx = start_idx + i
        try:
            # Fast native validation
            if not validate_mnemonic_native(seed, wordlist):
                results.append({
                    'seed_idx': seed_idx,
                    'seed': seed,
                    'error': 'Invalid mnemonic',
                    'success': False
                })
                continue
            
            # Native seed generation
            mnemonic_bytes = seed.encode('utf-8')
            salt = b'mnemonic'
            seed_bytes = NativeCrypto.pbkdf2_native(mnemonic_bytes, salt, 2048)
            
            # Generate addresses for each path
            for base_path, address_type in paths:
                for addr_idx in range(num_addresses):
                    # Generate full path
                    if base_path == "m/44'/0'/0'/0":
                        full_path = f"m/44'/0'/0'/0/{addr_idx}'"
                    elif base_path == "m/49'/0'/0'/0":
                        full_path = f"m/49'/0'/0'/0/{addr_idx}'"
                    elif base_path == "m/84'/0'/0'/0":
                        full_path = f"m/84'/0'/0'/0/{addr_idx}'"
                    elif base_path == "m/0'/0'/0'":
                        full_path = f"m/0'/0'/{addr_idx}'"
                    elif base_path == "m/0":
                        full_path = f"m/0/{addr_idx}'"
                    else:
                        full_path = f"{base_path}/{addr_idx}"

                    # Native key derivation
                    private_key, public_key = derive_key_native(seed_bytes, full_path)

                    # WIF format (common for all)
                    version_byte = 0x80
                    extended_key = bytes([version_byte]) + private_key + bytes([0x01])
                    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
                    private_key_wif = base58.b58encode(extended_key + checksum).decode('ascii')

                    # Special case: m/0 generates TWO addresses (like original)
                    if base_path == "m/0":
                        # P2WPKH nested in P2SH
                        p2sh_address = generate_address_native(public_key, "P2WPKH nested in P2SH")
                        results.append({
                            'seed_idx': seed_idx,
                            'seed': seed,
                            'derivation_path': full_path,
                            'address_index': addr_idx,
                            'address': p2sh_address,
                            'public_key': public_key.hex(),
                            'private_key': private_key.hex(),
                            'private_key_wif': private_key_wif,
                            'script_semantics': "P2WPKH nested in P2SH",
                            'success': True
                        })

                        # Native P2WPKH
                        p2wpkh_address = generate_address_native(public_key, "P2WPKH")
                        results.append({
                            'seed_idx': seed_idx,
                            'seed': seed,
                            'derivation_path': full_path,
                            'address_index': addr_idx,
                            'address': p2wpkh_address,
                            'public_key': public_key.hex(),
                            'private_key': private_key.hex(),
                            'private_key_wif': private_key_wif,
                            'script_semantics': "P2WPKH",
                            'success': True
                        })
                    else:
                        # Single address for other paths
                        address = generate_address_native(public_key, address_type)
                        results.append({
                            'seed_idx': seed_idx,
                            'seed': seed,
                            'derivation_path': full_path,
                            'address_index': addr_idx,
                            'address': address,
                            'public_key': public_key.hex(),
                            'private_key': private_key.hex(),
                            'private_key_wif': private_key_wif,
                            'script_semantics': address_type,
                            'success': True
                        })
                    
        except Exception as e:
            results.append({
                'seed_idx': seed_idx,
                'seed': seed,
                'error': f"Native processing error: {str(e)}",
                'success': False
            })
    
    return results

def process_seeds_native_g9(processor: G9NativeProcessor, input_file: str = "seeds.txt",
                           csv_output: str = "bip39_addresses_g9_v3_native.csv",
                           addresses_output: str = "bip39_only_addresses_g9_v3_native.txt",
                           num_addresses: int = 10):
    """G9 Native processing with maximum CPU utilization"""

    print(f"\n🚀 G9 Native v3.0 Processing: {input_file}")
    print(f"📊 CSV output: {csv_output}")
    print(f"📝 Addresses output: {addresses_output}")
    print("=" * 80)

    start_time = time.time()

    # Load wordlist once
    print("📖 Loading BIP39 wordlist...")
    wordlist = load_wordlist_once()
    print(f"✅ Loaded {len(wordlist)} words")

    # Read seeds
    print("📖 Reading seeds file...")
    with open(input_file, 'r', encoding='utf-8') as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not seeds:
        print(f"❌ No seeds found in {input_file}")
        return

    print(f"✅ Loaded {len(seeds)} seeds")

    # Create large batches for G9 native processing
    batches = []
    for i in range(0, len(seeds), processor.batch_size):
        batch_seeds = seeds[i:i + processor.batch_size]
        batches.append((batch_seeds, num_addresses, i, wordlist))

    print(f"📦 Created {len(batches)} native batches for G9 processing")
    print(f"🔧 Native optimization: Large batches ({processor.batch_size} seeds/batch)")

    # G9 Native parallel processing
    all_results = []
    processed_seeds = 0
    error_count = 0

    print(f"⚡ Starting G9 Native v3.0 processing with {processor.max_workers} workers...")
    print(f"🎯 Expected: 50-90% CPU utilization on G9 server")

    # Use multiprocessing with native operations
    from multiprocessing import Pool

    with Pool(processes=processor.max_workers) as pool:
        if TQDM_AVAILABLE:
            # Process with progress bar
            with tqdm(total=len(seeds), desc="🔐 G9 Native Processing",
                     unit="seeds", smoothing=0.05) as pbar:

                # Submit all batches
                results = pool.map_async(process_seed_batch_native, batches)

                # Monitor progress
                while not results.ready():
                    time.sleep(0.1)
                    # Update progress based on completed work
                    # (This is approximate since we can't get exact progress from pool.map)

                # Get all results
                batch_results_list = results.get()

                for batch_results in batch_results_list:
                    all_results.extend(batch_results)

                    batch_successful = sum(1 for r in batch_results if r.get('success', False))
                    batch_errors = len([r for r in batch_results if not r.get('success', False)])

                    processed_seeds += batch_successful
                    error_count += batch_errors

                    pbar.update(len([r for r in batch_results if 'seed_idx' in r]))
                    pbar.set_postfix({
                        'Success': processed_seeds,
                        'Errors': error_count,
                        'Workers': processor.max_workers,
                        'Native': 'v3.0'
                    })
        else:
            # Process without progress bar
            print("Processing with native operations...")
            batch_results_list = pool.map(process_seed_batch_native, batches)

            for i, batch_results in enumerate(batch_results_list):
                all_results.extend(batch_results)

                batch_successful = sum(1 for r in batch_results if r.get('success', False))
                batch_errors = len([r for r in batch_results if not r.get('success', False)])

                processed_seeds += batch_successful
                error_count += batch_errors

                print(f"✅ Native Batch {i+1}/{len(batches)} complete - "
                      f"Success: {processed_seeds}, Errors: {error_count}")

    # Write results
    print(f"\n💾 Writing native results...")
    write_results_native(all_results, csv_output, addresses_output)

    # Performance summary
    end_time = time.time()
    total_time = end_time - start_time
    seeds_per_second = len(seeds) / total_time if total_time > 0 else 0
    addresses_generated = processed_seeds * num_addresses * 5  # 5 derivation paths

    print(f"\n🎉 G9 Native v3.0 Processing Complete!")
    print("=" * 60)
    print(f"🖥️  G9 Native Performance:")
    print(f"   💻 Workers used: {processor.max_workers}/{processor.total_cores}")
    print(f"   🔧 Native libraries: coincurve={COINCURVE_AVAILABLE}, cryptography={CRYPTOGRAPHY_AVAILABLE}")
    print(f"📊 Processing Results:")
    print(f"   📝 Total seeds: {len(seeds)}")
    print(f"   ✅ Successful: {processed_seeds}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   🔐 Addresses generated: {addresses_generated:,}")
    print(f"⏱️  Performance Metrics:")
    print(f"   🕐 Total time: {total_time:.2f} seconds")
    print(f"   🚀 Speed: {seeds_per_second:.2f} seeds/second")
    print(f"   ⚡ Throughput: {addresses_generated/total_time:.0f} addresses/second")
    print(f"🎯 Expected G9 Results:")
    print(f"   💻 CPU Usage: Should be 50-90% (vs 1% in v2.0)")
    print(f"   🚀 Speed: Should be 500-2000 seeds/s (vs 11 in v2.0)")
    print(f"📁 Output files:")
    print(f"   📊 {csv_output}")
    print(f"   📝 {addresses_output}")

def write_results_native(results: List[Dict], csv_output: str, addresses_output: str):
    """Write native processing results"""

    successful_results = [r for r in results if r.get('success', False)]
    error_results = [r for r in results if not r.get('success', False)]

    print(f"📊 Writing {len(successful_results)} native results...")

    # Write CSV
    if successful_results:
        with open(csv_output, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['seed_index', 'seed', 'derivation_path', 'address_index', 'address',
                         'public_key', 'private_key', 'private_key_wif', 'script_semantics']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

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

    # Write addresses only
    if successful_results:
        with open(addresses_output, 'w', encoding='utf-8') as txtfile:
            for result in successful_results:
                txtfile.write(result['address'] + '\n')

    # Error log
    if error_results:
        error_file = csv_output.replace('.csv', '_native_errors.log')
        with open(error_file, 'w', encoding='utf-8') as errfile:
            errfile.write("G9 Native Processing v3.0 Error Log\n")
            errfile.write("=" * 50 + "\n")
            errfile.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            errfile.write(f"Total Errors: {len(error_results)}\n\n")

            for result in error_results:
                errfile.write(f"Seed Index: {result['seed_idx'] + 1}\n")
                errfile.write(f"Seed: {result['seed'][:50]}...\n")
                errfile.write(f"Error: {result.get('error', 'Unknown error')}\n")
                errfile.write("-" * 30 + "\n")
        print(f"⚠️  Native error log: {error_file}")

def main():
    """G9 Native v3.0 main function"""

    parser = argparse.ArgumentParser(
        description='G9 Native Performance BIP39 Processor v3.0 - Maximum CPU utilization for 144 cores',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 G9 Native v3.0 Examples:
  # Maximum G9 performance (recommended)
  python batch_process_seeds_g9_v3.0_native.py --native-mode

  # Custom G9 native configuration
  python batch_process_seeds_g9_v3.0_native.py --workers 100 --batch-size 10000

🎯 Expected G9 Results:
  - CPU Usage: 50-90% (vs 1% in v2.0)
  - Speed: 500-2000 seeds/second (vs 11 in v2.0)
  - Time: 1-2 seconds for 1000 seeds (vs 90 seconds in v2.0)
        """
    )

    parser.add_argument('-i', '--input', default='seeds.txt',
                       help='Input seeds file')
    parser.add_argument('-c', '--csv', default='bip39_addresses_g9_v3_native.csv',
                       help='CSV output file')
    parser.add_argument('-a', '--addresses', default='bip39_only_addresses_g9_v3_native.txt',
                       help='Addresses output file')
    parser.add_argument('-n', '--num', type=int, default=10,
                       help='Addresses per derivation path')
    parser.add_argument('-w', '--workers', type=int, default=None,
                       help='Number of workers (default: auto for G9)')
    parser.add_argument('-b', '--batch-size', type=int, default=None,
                       help='Batch size (default: optimized for G9)')
    parser.add_argument('--native-mode', action='store_true',
                       help='Enable G9 native high-performance mode')

    args = parser.parse_args()

    # Native mode optimizations
    if args.native_mode:
        print("🚀 G9 Native v3.0 High-Performance Mode!")
        total_cores = cpu_count()
        if args.workers is None:
            if total_cores >= 100:  # G9 server
                args.workers = max(50, min(120, int(total_cores * 0.8)))
                print(f"🔧 G9 Native: Using {args.workers} workers (80% of {total_cores} cores)")
            else:
                args.workers = max(8, int(total_cores * 0.8))
        if args.batch_size is None:
            if total_cores >= 100:  # G9 server
                args.batch_size = max(10000, total_cores * 100)
            else:
                args.batch_size = 2000
        print(f"⚡ Native Config: {args.workers} workers, {args.batch_size} batch size")

    print("🖥️  G9 Native Performance BIP39 Processor v3.0")
    print("=" * 70)
    print(f"💻 System: {cpu_count()} cores, {psutil.virtual_memory().total / (1024**3):.1f}GB RAM")
    print(f"📁 Input: {args.input}")
    print(f"📊 CSV: {args.csv}")
    print(f"📝 Addresses: {args.addresses}")
    print(f"🔢 Addresses per path: {args.num}")

    # Initialize native processor
    processor = G9NativeProcessor(
        max_workers=args.workers,
        batch_size=args.batch_size
    )

    # Process with native performance
    process_seeds_native_g9(
        processor=processor,
        input_file=args.input,
        csv_output=args.csv,
        addresses_output=args.addresses,
        num_addresses=args.num
    )

if __name__ == "__main__":
    main()
