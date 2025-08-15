@echo off
echo BIP39 Offline Address Generator
echo ================================
echo.
echo This tool will help you generate Bitcoin addresses from your BIP39 mnemonic phrase.
echo.
echo SECURITY WARNING:
echo - Disconnect from the internet before entering your real mnemonic phrase
echo - Never share your mnemonic phrase or private keys with anyone
echo - Test with small amounts first
echo.
pause
echo.
python bip39_interactive.py
echo.
echo Process completed. Check the generated CSV file for your addresses.
pause
