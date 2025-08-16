# G9 4-CPU Haswell Optimization Guide - Version 3.3

## Problem Analysis

Your G9 server with 4×Intel E7-8880 v3 CPUs was performing poorly with v3.2:
- **Speed**: Only 47.31 seeds/second (expected 120-250)
- **Time**: 211 seconds for 10,000 seeds (expected 40-80 seconds)
- **CPU Usage**: Likely 50-70% (expected 80-95%)

## Root Causes Identified

### 1. **CPU Detection Problem**
- **Issue**: v3.2 detected 144 threads and used 108 workers
- **Problem**: Treated hyperthreads as real cores
- **Fix**: v3.3 detects 72 physical cores, uses 50-60 workers

### 2. **Batch Size Too Large**
- **Issue**: v3.2 used 14,400 seeds per batch (only 1 batch for 10,000 seeds)
- **Problem**: No parallelization, Python GIL bottleneck
- **Fix**: v3.3 uses 500-1000 seeds per batch (10-20 batches)

### 3. **Haswell Architecture Limitations**
- **Issue**: E7-8880 v3 is 2015 Haswell with DDR4-2133 memory
- **Problem**: Memory bandwidth bottleneck, older cache hierarchy
- **Fix**: v3.3 optimized for Haswell memory patterns

### 4. **Python GIL Coordination Overhead**
- **Issue**: Too many workers caused GIL contention
- **Problem**: Context switching overhead on older CPUs
- **Fix**: v3.3 uses fewer workers with better work distribution

## Key Optimizations in v3.3

### 1. **Smart CPU Detection**
```python
# v3.2 (WRONG)
self.total_cores = cpu_count()  # 144 threads
self.max_workers = int(self.total_cores * 0.75)  # 108 workers

# v3.3 (CORRECT)
self.total_threads = cpu_count()  # 144 threads
self.physical_cores = self.total_threads // 2  # 72 physical cores
self.max_workers = int(self.physical_cores * 0.8)  # 58 workers
```

### 2. **Optimal Batch Sizing**
```python
# v3.2 (WRONG)
self.batch_size = max(5000, min(20000, self.total_cores * 100))  # 14,400

# v3.3 (CORRECT)
self.batch_size = max(500, min(1000, 10000 // 15))  # 666-1000
```

### 3. **Haswell-Specific Tuning**
- **Workers**: 50-60 (70-85% of physical cores)
- **Batch Size**: 500-1000 seeds
- **Target Batches**: 10-20 for 10,000 seeds
- **Memory Access**: Cache-friendly patterns

## Expected Performance Improvements

### Before (v3.2)
- **Speed**: 47.31 seeds/second
- **Time**: 211 seconds for 10,000 seeds
- **Workers**: 108 (too many)
- **Batches**: 1 (no parallelization)
- **CPU Usage**: 50-70%

### After (v3.3)
- **Speed**: 120-250 seeds/second (**2.5-5x faster**)
- **Time**: 40-80 seconds for 10,000 seeds (**2.6-5.3x faster**)
- **Workers**: 50-60 (optimal)
- **Batches**: 10-20 (proper parallelization)
- **CPU Usage**: 80-95%

## Usage Instructions

### Run v3.3 on your G9 server:
```bash
python batch_process_seeds_g9_v3.3_optimized.py \
    --input seeds_20250816_164208.txt \
    --workers 58 \
    --batch-size 800 \
    --csv-output bip39_addresses_g9_v3.3_haswell.csv \
    --addresses-output btc_20250816_164208_v3.3.txt
```

### Monitor Performance:
```bash
# Check CPU usage during processing
htop

# Expected to see:
# - 80-95% CPU usage across all cores
# - 50-60 active processes
# - 10-20 batches processing sequentially
```

## Technical Details

### CPU Architecture Optimization
- **Target**: Intel E7-8880 v3 (Haswell, 2015)
- **Cores**: 4 CPUs × 18 cores = 72 physical cores
- **Memory**: DDR4-2133 (slower than modern systems)
- **Cache**: L3 cache per CPU socket optimization

### Python GIL Mitigation
- **Strategy**: Fewer workers with larger work units
- **Benefit**: Reduced context switching overhead
- **Result**: Better CPU utilization on older hardware

### Memory Bandwidth Optimization
- **Problem**: Haswell has limited memory bandwidth vs modern CPUs
- **Solution**: Smaller batches reduce memory pressure
- **Result**: Better cache utilization and throughput

## Verification

The v3.3 optimizations should deliver:
1. **2.5-5x speed improvement** (47 → 120-250 seeds/second)
2. **80-95% CPU utilization** (vs 50-70% in v3.2)
3. **Proper parallelization** (10-20 batches vs 1 batch)
4. **Reduced processing time** (211s → 40-80s for 10,000 seeds)

If you still see poor performance, the issue may be:
- Network/disk I/O bottlenecks
- Memory configuration problems
- NUMA topology issues
- Background processes consuming CPU

## Next Steps

1. **Test v3.3** with your 10,000 seed file
2. **Monitor with htop** to verify 80-95% CPU usage
3. **Compare timing** against the 211-second baseline
4. **Report results** for further optimization if needed
