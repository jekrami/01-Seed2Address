# Version 3.4 Changelog - August 19, 2025

## Summary
Version 3.4 fixes the derivation path format to match standard BIP specifications and produces the exact expected output format.

## Changes Made Today (2025-08-19)

### 🔧 **Path Format Corrections**
**Issue**: v3.3 was generating incorrect derivation paths that didn't match expected output.

**Fixed Paths**:
- ✅ `m/0/0` and `m/0/1` (was `m/0/0'` and `m/0/1'`)
- ✅ `m/44'/0'/0'/0/0` and `m/44'/0'/0'/0/1` (was `m/44'/0'/0'/0/0'` and `m/44'/0'/0'/0/1'`)
- ✅ `m/49'/0'/0'/0/0` and `m/49'/0'/0'/0/1` (was `m/49'/0'/0'/0/0'` and `m/49'/0'/0'/0/1'`)
- ✅ `m/84'/0'/0'/0/0` and `m/84'/0'/0'/0/1` (was `m/84'/0'/0'/0/0'` and `m/84'/0'/0'/0/1'`)

### 📝 **Expected Output Verification**
**Test Seed**: `hard split scrap crater tomorrow during panda shoot adjust glance prepare hawk`

**Generated Results Match Expected**:

| Path | Address | Public Key | Private Key WIF |
|------|---------|------------|-----------------|
| m/0/0 | 1PaL9hZ5iTareT4Gg9fxwHDXEudwyWpfCp | 0214794e865781d2990b3a939ffcc20e7f3cb3e6172c45b8996d3b5ed08cf6ad4a | KzTJEkSQWmb74U58fKFtm7A41Am4tZ599e21g7myzdN7GBraW5Yo |
| m/0/1 | 1HMsQsMwTE3Qi335WF7vcWghreJmey8fTd | 024e7b21ff6bc4e2c6a465e4616bc1603e08e7943092da28c8ea49f0b0fd59e143 | L525mb8Z5QG4KCGmN3jhLcxCVMM7ybCY1YoRo2RwTN2YLYYJ9dt7 |
| m/44'/0'/0'/0/0 | 1MbGy15SNnG2fmd6gSqzuwUrfsqBtDP9y4 | 02cc25b8f82af473d3099547dc2d8ed5a2bb561393c533909edeb85bab570ffa6a | L3peh2sYyDJ8AR4rtEyPxKBMcYha4VdkqZGcGorXCx3S4otTVk7q |
| m/44'/0'/0'/0/1 | 1WWyV7cLaaDkHh756y7F9gqirLoz2ggmH | 03072075e7cf138fcd244f994a1aa746c6d4ef40b4ec351dcad11c2db3ab48d7d9 | KzJLjGEoDirfoziEWcq48HcKFz7KLh6ZYceyYNPYeNQ3o6yyJwxm |
| m/49'/0'/0'/0/0 | 3BdhNs13RvPKmWtUsTA3vW7tgtJ7AJ4shh | 037efa60ee5a645fa10e5f764b482e9542d2a931a6ecf7df939cb0ba549d9b3312 | Ky3mDCvS6eSCvDMDpkBoLWBEZicVnJ6fbrtYCUiYv2YbzBJ9C1dW |
| m/49'/0'/0'/0/1 | 39aSarGVpH4qG7uLEX3NGfGXiqtWNBGggS | 0239043131e7dce9a1665119b975324b8b3bafb722d95adcd5c6f18b3d3b0af55a | KyXcK713dk8aZAYSu3ZJRLTFNYHFf2tcAWkzWrCqsfCVNuQJVMqb |
| m/84'/0'/0'/0/0 | bc1qks3tql08hs2n977z204s6292n0qplm6afuj4we | 025ec3a2e6b6f156ba9f6ae943439644b977e9043c2053bea73f038ea9a5178ef9 | KxWL1gYSMncF9GvgPqi3bKt3QAm5irCpNerhPYkPowskkfxDM9cg |
| m/84'/0'/0'/0/1 | bc1q9zqssm4k4gvqvngdr0t2dw6z7qqwt4w69576cf | 02b23780bc9d587c3a5cb1253e879462b861660fe0dd5599e1e4366676193de475 | L5A1Fict6xCiG2AmHcocGprkUyhCRCMcfJfKtNjmV8NZRBq8ccAZ |

**P2WPKH nested in P2SH**:
| Path | Address | Public Key | Private Key WIF |
|------|---------|------------|-----------------|
| m/0/0 | 393LtWtTbBjiXbzCPCYKTxWi8CdTtCLhhv | 0214794e865781d2990b3a939ffcc20e7f3cb3e6172c45b8996d3b5ed08cf6ad4a | KzTJEkSQWmb74U58fKFtm7A41Am4tZ599e21g7myzdN7GBraW5Yo |
| m/0/1 | 3AS8kTUcsuLE4VGYPXbGbKZub2iTw46UYb | 024e7b21ff6bc4e2c6a465e4616bc1603e08e7943092da28c8ea49f0b0fd59e143 | L525mb8Z5QG4KCGmN3jhLcxCVMM7ybCY1YoRo2RwTN2YLYYJ9dt7 |

**P2WPKH**:
| Path | Address | Public Key | Private Key WIF |
|------|---------|------------|-----------------|
| m/0/0 | bc1q77s843savwheermfxmxyt3hkuz4kjf46t2esel | 0214794e865781d2990b3a939ffcc20e7f3cb3e6172c45b8996d3b5ed08cf6ad4a | KzTJEkSQWmb74U58fKFtm7A41Am4tZ599e21g7myzdN7GBraW5Yo |
| m/0/1 | bc1qkd6xn3ene7gs7hn20qt4mg2rggdfrgfhw5s8mq | 024e7b21ff6bc4e2c6a465e4616bc1603e08e7943092da28c8ea49f0b0fd59e143 | L525mb8Z5QG4KCGmN3jhLcxCVMM7ybCY1YoRo2RwTN2YLYYJ9dt7 |

### 🔧 **Technical Changes**

**Path Definition Updates**:
```python
# v3.3 (INCORRECT)
("m/0", "P2PKH", lambda i: f"{i}'"),  # Generated m/0/0', m/0/1'

# v3.4 (CORRECT)
("m/0", "P2PKH", lambda i: str(i)),   # Generates m/0/0, m/0/1
```

**BIP Standard Compliance**:
- **BIP44**: `m/44'/0'/0'/0/x` (non-hardened final index)
- **BIP49**: `m/49'/0'/0'/0/x` (non-hardened final index)  
- **BIP84**: `m/84'/0'/0'/0/x` (non-hardened final index)
- **Simple**: `m/0/x` (non-hardened derivation)

### 🚀 **Performance Maintained**
All Haswell optimizations from v3.3 are preserved:
- ✅ 50-60 workers (70-85% of physical cores)
- ✅ 500-1000 batch size for better parallelization
- ✅ Memory locality optimization for DDR4-2133
- ✅ Reduced Python GIL contention

### 📁 **Files Created**
- `batch_process_seeds_g9_v3.4_optimized.py` - The corrected version
- `VERSION_3.4_CHANGELOG_2025-08-19.md` - This changelog

### 🎯 **Usage**
```bash
python batch_process_seeds_g9_v3.4_optimized.py \
    --input your_seeds.txt \
    --workers 58 \
    --batch-size 800 \
    --csv-output results_v3.4.csv
```

### ✅ **Verification**
Version 3.4 now produces **100% accurate results** that match the expected output format exactly.

## Summary of All Versions

| Version | Date | Key Changes |
|---------|------|-------------|
| v3.2 | 2025-08-16 | Fixed cryptographic functions, but had performance issues |
| v3.3 | 2025-08-16 | Fixed Haswell performance optimizations |
| v3.4 | 2025-08-19 | **Fixed derivation path format to match BIP standards** |

**Recommendation**: Use v3.4 for production - it combines correct output format with optimal G9 performance.