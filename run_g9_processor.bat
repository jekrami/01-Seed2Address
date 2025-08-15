@echo off
echo ========================================
echo HP G9 Enhanced BIP39 Seed Processor
echo ========================================
echo.
echo This script runs the G9-optimized version
echo designed for HP G9 servers with 140+ cores
echo and 256GB RAM.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python detected. Starting G9 processor...
echo.

REM Run with G9 high-performance mode
python batch_process_seeds_g9.py --g9-mode

echo.
echo ========================================
echo G9 Processing Complete!
echo ========================================
echo.
echo Output files generated:
echo - bip39_addresses_g9.csv (full data)
echo - bip39_only_addresses_g9.txt (addresses only)
echo.
pause
