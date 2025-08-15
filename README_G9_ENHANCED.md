# HP G9 Enhanced BIP39 Batch Seed Processor

## 🚀 Optimized for HP G9 Servers

This enhanced version is specifically designed for HP G9 servers with:
- **140+ CPU cores**
- **256GB RAM**
- **High-performance parallel processing**

## ✨ Key Features

### 🔧 G9 Optimizations
- **Advanced Multiprocessing**: Utilizes up to 85% of available cores (120+ cores on G9)
- **Intelligent Memory Management**: Optimized for 256GB RAM with dynamic batch sizing
- **Real-time Performance Monitoring**: Live CPU, memory, and throughput tracking
- **Enhanced Error Handling**: Comprehensive error logging and recovery
- **Optimized I/O**: High-performance file operations with buffering

### 📊 Performance Enhancements
- **Parallel Processing**: ProcessPoolExecutor with optimal worker management
- **Batch Optimization**: Dynamic batch sizing based on system resources
- **Memory Efficiency**: Smart memory usage to prevent system overload
- **Progress Tracking**: Real-time progress bars with performance metrics

## 🚀 Quick Start

### Basic Usage (Recommended)
```bash
# Run with G9 high-performance mode
python batch_process_seeds_g9.py --g9-mode
```

### Using Batch File
```bash
# Windows batch file for easy execution
run_g9_processor.bat
```

## 📋 Command Line Options

### Basic Options
```bash
python batch_process_seeds_g9.py [options]

-i, --input          Input file (default: seeds.txt)
-c, --csv            CSV output file (default: bip39_addresses_g9.csv)
-a, --addresses      Addresses output file (default: bip39_only_addresses_g9.txt)
-n, --num            Addresses per derivation path (default: 10)
```

### G9 Performance Options
```bash
-w, --workers        Number of worker processes (default: auto-detect for G9)
-b, --batch-size     Batch size for processing (default: G9 optimized)
-m, --memory-limit   Memory limit in GB (default: 220)
--g9-mode           Enable G9 high-performance mode (recommended)
--benchmark         Run G9 performance benchmark
```

## 🔥 G9 Usage Examples

### High-Performance Mode (Recommended)
```bash
# Optimal settings for G9 server
python batch_process_seeds_g9.py --g9-mode
```

### Custom G9 Configuration
```bash
# Custom worker and batch configuration
python batch_process_seeds_g9.py --workers 120 --batch-size 2000 --memory-limit 200
```

### Large File Processing
```bash
# Process large seed files with G9 optimization
python batch_process_seeds_g9.py -i large_seeds.txt --g9-mode --memory-limit 220
```

### Performance Benchmark
```bash
# Test G9 system performance
python batch_process_seeds_g9.py --benchmark
```

## 📊 Performance Metrics

### Expected G9 Performance
- **Processing Speed**: 50-100+ seeds/second (depending on configuration)
- **Memory Usage**: 60-80% of 256GB RAM (optimized)
- **CPU Utilization**: 80-85% of 140+ cores
- **Throughput**: 10,000+ addresses/second

### Real-time Monitoring
The G9 version provides real-time monitoring of:
- Processing speed (seeds/second)
- Memory usage percentage
- CPU utilization
- Active worker processes
- Error rates

## 📁 Output Files

### Standard Outputs
- `bip39_addresses_g9.csv` - Complete data with all fields
- `bip39_only_addresses_g9.txt` - Addresses only for balance checking
- `bip39_addresses_g9_errors.log` - Error log (if errors occur)

### File Formats
The G9 version maintains compatibility with the original format while adding enhanced error logging and performance metrics.

## 🔧 System Requirements

### Minimum Requirements
- Python 3.7+
- 8GB RAM
- 4+ CPU cores

### Recommended for G9
- Python 3.9+
- HP G9 server with 140+ cores
- 256GB RAM
- SSD storage for optimal I/O

### Dependencies
```bash
# Required
pip install psutil

# Optional (for progress bars)
pip install tqdm
```

## ⚡ G9 Optimization Details

### Multiprocessing Strategy
- Uses ProcessPoolExecutor for optimal resource management
- Dynamic worker allocation based on system capabilities
- Intelligent batch distribution to minimize overhead

### Memory Management
- Monitors real-time memory usage
- Dynamic batch sizing to prevent memory exhaustion
- Efficient result aggregation and writing

### Performance Monitoring
- Background monitoring thread
- Real-time CPU and memory tracking
- Performance statistics and reporting

## 🛠️ Troubleshooting

### Common Issues
1. **High Memory Usage**: Reduce batch size or memory limit
2. **Slow Performance**: Enable G9 mode or increase workers
3. **Process Errors**: Check error log file for details

### G9 Specific Tips
- Use `--g9-mode` for optimal performance
- Monitor system resources during processing
- Adjust memory limit based on other running processes

## 📈 Comparison with Original

| Feature | Original | G9 Enhanced |
|---------|----------|-------------|
| Processing | Sequential | Parallel (140+ cores) |
| Memory Usage | Basic | Optimized (256GB) |
| Monitoring | None | Real-time |
| Error Handling | Basic | Enhanced |
| Performance | ~1-5 seeds/sec | 50-100+ seeds/sec |
| Scalability | Limited | G9 Optimized |

## 🎯 Best Practices for G9

1. **Use G9 Mode**: Always use `--g9-mode` for optimal performance
2. **Monitor Resources**: Watch memory and CPU usage during processing
3. **Batch Processing**: Process large files in chunks if needed
4. **Error Handling**: Review error logs for any processing issues
5. **Performance Testing**: Run benchmark to optimize settings

## 📞 Support

For G9-specific issues or optimization questions, refer to the error logs and performance metrics provided by the enhanced monitoring system.
