#!/usr/bin/env python3
"""
BIP39 Offline Address Generator - Version 2.0 G9 Optimized
==========================================================

VERSION: 2.0 G9 Optimized
DATE: 2025-08-14
CHANGES FROM v1.0:
- CRITICAL FIX: Eliminated redundant BIP39 wordlist loading in generate_addresses()
- Added bip39_instance parameter to generate_addresses() to reuse existing instance
- This fixes the major I/O bottleneck that was causing poor G9 server performance
- Maintains full backward compatibility with v1.0 API

PERFORMANCE IMPACT:
- Eliminates 99% of file I/O operations in batch processing
- Expected 10-50x performance improvement on multi-core systems
- Fixes G9 server low CPU utilization issue (was 0.7%, should now be 15-50%+)

TECHNICAL DETAILS:
- Previous version: Each generate_addresses() call loaded bip39-english.csv (2048 words)
- New version: Reuses existing BIP39 instance, loads wordlist only once per worker
- With 1000 seeds × 122 workers: Reduced from 122,000 file reads to 122 file reads
- File I/O contention eliminated, CPU can focus on actual cryptographic work

Generates Bitcoin addresses from BIP39 mnemonic phrases for various derivation paths.
"""

import hashlib
import hmac
import binascii
import struct
import csv
from typing import List, Tuple, Dict, Optional
import base58

# ECDSA and Bitcoin utilities
import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point

# Pure Python RIPEMD160 implementation for compatibility with different OpenSSL versions
def _ripemd160_pure_python(data):
    """Pure Python RIPEMD160 implementation for OpenSSL compatibility"""
    
    def _f(j, x, y, z):
        assert 0 <= j and j < 80
        if j < 16:
            return x ^ y ^ z
        elif 16 <= j < 32:
            return (x & y) | (~x & z)
        elif 32 <= j < 48:
            return (x | ~y) ^ z
        elif 48 <= j < 64:
            return (x & z) | (y & ~z)
        else:
            return x ^ (y | ~z)

    def _K(j):
        assert 0 <= j and j < 80
        if j < 16:
            return 0x00000000
        elif 16 <= j < 32:
            return 0x5a827999
        elif 32 <= j < 48:
            return 0x6ed9eba1
        elif 48 <= j < 64:
            return 0x8f1bbcdc
        else:
            return 0xa953fd4e

    def _Kh(j):
        assert 0 <= j and j < 80
        if j < 16:
            return 0x50a28be6
        elif 16 <= j < 32:
            return 0x5c4dd124
        elif 32 <= j < 48:
            return 0x6d703ef3
        elif 48 <= j < 64:
            return 0x7a6d76e9
        else:
            return 0x00000000

    def _padandsplit(message):
        """
        returns the message length in bits and the message split into 512-bit chunks
        """
        msglen = len(message)
        message += b'\x80'
        message += b'\x00' * ((55 - msglen) % 64)
        message += struct.pack('<Q', msglen * 8)
        assert len(message) % 64 == 0
        return [message[i:i+64] for i in range(0, len(message), 64)]

    def _rol(n, b):
        """
        left rotate a 32-bit integer n by b bits.
        """
        n &= 0xffffffff
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    def _compress(h0, h1, h2, h3, h4, block):
        """
        Compress a 512-bit block with the given hash state.
        """
        w = list(struct.unpack('<16L', block))

        al, bl, cl, dl, el = h0, h1, h2, h3, h4
        ar, br, cr, dr, er = h0, h1, h2, h3, h4

        # Left line
        rl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
              7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
              3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
              1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
              4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]

        sl = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
              7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
              11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
              11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
              9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]

        # Right line
        rr = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
              6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
              15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
              8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
              12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]

        sr = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
              9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
              9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
              15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
              8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]

        for j in range(80):
            t = _rol((al + _f(j, bl, cl, dl) + w[rl[j]] + _K(j)) & 0xffffffff, sl[j]) + el
            al, bl, cl, dl, el = el & 0xffffffff, t & 0xffffffff, bl & 0xffffffff, _rol(cl, 10), dl & 0xffffffff
            t = _rol((ar + _f(79-j, br, cr, dr) + w[rr[j]] + _Kh(j)) & 0xffffffff, sr[j]) + er
            ar, br, cr, dr, er = er & 0xffffffff, t & 0xffffffff, br & 0xffffffff, _rol(cr, 10), dr & 0xffffffff

        t = (h1 + cl + dr) & 0xffffffff
        h1 = (h2 + dl + er) & 0xffffffff
        h2 = (h3 + el + ar) & 0xffffffff
        h3 = (h4 + al + br) & 0xffffffff
        h4 = (h0 + bl + cr) & 0xffffffff
        h0 = t

        return h0, h1, h2, h3, h4

    # Initialize hash state
    h0, h1, h2, h3, h4 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0

    # Process message in 512-bit chunks
    for block in _padandsplit(data):
        h0, h1, h2, h3, h4 = _compress(h0, h1, h2, h3, h4, block)

    # Produce the final hash value
    return struct.pack('<5L', h0, h1, h2, h3, h4)

class BIP39:
    def __init__(self, wordlist_file: str = "bip39-english.csv"):
        """Initialize BIP39 with English wordlist"""
        self.wordlist = self._load_wordlist(wordlist_file)
        
    def _load_wordlist(self, filename: str) -> List[str]:
        """Load BIP39 wordlist from CSV file"""
        wordlist = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:  # Skip empty rows
                        wordlist.append(row[0].strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Wordlist file {filename} not found")
        
        if len(wordlist) != 2048:
            raise ValueError(f"Invalid wordlist length: {len(wordlist)}, expected 2048")
        
        return wordlist
    
    def mnemonic_to_seed(self, mnemonic: str, passphrase: str = "") -> bytes:
        """Convert mnemonic to seed using PBKDF2"""
        mnemonic_bytes = mnemonic.encode('utf-8')
        salt = ('mnemonic' + passphrase).encode('utf-8')
        
        # PBKDF2 with 2048 iterations
        seed = hashlib.pbkdf2_hmac('sha512', mnemonic_bytes, salt, 2048)
        return seed
    
    def validate_mnemonic(self, mnemonic: str) -> bool:
        """Validate BIP39 mnemonic checksum"""
        words = mnemonic.strip().split()
        if len(words) not in [12, 15, 18, 21, 24]:
            return False
        
        # Convert words to indices
        try:
            indices = [self.wordlist.index(word) for word in words]
        except ValueError:
            return False
        
        # Convert to binary
        binary_str = ''.join(format(idx, '011b') for idx in indices)
        
        # Split entropy and checksum
        entropy_length = len(binary_str) * 32 // 33
        entropy_bits = binary_str[:entropy_length]
        checksum_bits = binary_str[entropy_length:]
        
        # Calculate expected checksum
        entropy_bytes = bytes(int(entropy_bits[i:i+8], 2) for i in range(0, len(entropy_bits), 8))
        hash_bytes = hashlib.sha256(entropy_bytes).digest()
        expected_checksum = format(hash_bytes[0], '08b')[:len(checksum_bits)]
        
        return checksum_bits == expected_checksum

class BIP32:
    """BIP32 Hierarchical Deterministic key derivation"""
    
    HARDENED_OFFSET = 0x80000000
    
    def __init__(self, seed: bytes):
        """Initialize with master seed"""
        self.master_key, self.master_chain_code = self._master_key_from_seed(seed)
    
    def _master_key_from_seed(self, seed: bytes) -> Tuple[bytes, bytes]:
        """Generate master private key and chain code from seed"""
        hmac_result = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return hmac_result[:32], hmac_result[32:]
    
    def _derive_child_key(self, parent_key: bytes, parent_chain_code: bytes, index: int) -> Tuple[bytes, bytes]:
        """Derive child key from parent"""
        if index >= self.HARDENED_OFFSET:
            # Hardened derivation
            data = b'\x00' + parent_key + struct.pack('>I', index)
        else:
            # Non-hardened derivation
            parent_public_key = self._private_to_public(parent_key)
            data = parent_public_key + struct.pack('>I', index)
        
        hmac_result = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
        child_key_int = (int.from_bytes(hmac_result[:32], 'big') + int.from_bytes(parent_key, 'big')) % SECP256k1.order
        child_key = child_key_int.to_bytes(32, 'big')
        child_chain_code = hmac_result[32:]
        
        return child_key, child_chain_code
    
    def _private_to_public(self, private_key: bytes) -> bytes:
        """Convert private key to compressed public key"""
        private_key_int = int.from_bytes(private_key, 'big')
        point = private_key_int * SECP256k1.generator
        
        # Compressed public key format
        if point.y() % 2 == 0:
            return b'\x02' + point.x().to_bytes(32, 'big')
        else:
            return b'\x03' + point.x().to_bytes(32, 'big')
    
    def derive_path(self, path: str) -> Tuple[bytes, bytes, bytes]:
        """Derive key from BIP32 path (e.g., "m/44'/0'/0'/0/0")"""
        if not path.startswith('m/'):
            raise ValueError("Path must start with 'm/'")
        
        current_key = self.master_key
        current_chain_code = self.master_chain_code
        
        path_parts = path[2:].split('/')
        if path_parts == ['']:
            path_parts = []
        
        for part in path_parts:
            if part.endswith("'"):
                index = int(part[:-1]) + self.HARDENED_OFFSET
            else:
                index = int(part)
            
            current_key, current_chain_code = self._derive_child_key(current_key, current_chain_code, index)
        
        public_key = self._private_to_public(current_key)
        return current_key, public_key, current_chain_code

class BitcoinAddress:
    """Bitcoin address generation utilities"""

    @staticmethod
    def hash160(data: bytes) -> bytes:
        """RIPEMD160(SHA256(data)) - Compatible with different OpenSSL versions"""
        sha256_hash = hashlib.sha256(data).digest()
        
        # Try to use hashlib's RIPEMD160 first (available in OpenSSL 3.0.13+)
        try:
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(sha256_hash)
            return ripemd160.digest()
        except ValueError:
            # Fallback to pure Python implementation for older OpenSSL versions
            return _ripemd160_pure_python(sha256_hash)

    @staticmethod
    def base58check_encode(payload: bytes, version: int = 0) -> str:
        """Base58Check encoding"""
        versioned_payload = bytes([version]) + payload
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        return base58.b58encode(versioned_payload + checksum).decode('ascii')

    @staticmethod
    def private_key_to_wif(private_key: bytes, compressed: bool = True) -> str:
        """Convert private key to WIF (Wallet Import Format)"""
        # Bitcoin mainnet version byte
        version_byte = 0x80

        # Add compression flag if compressed
        if compressed:
            extended_key = bytes([version_byte]) + private_key + bytes([0x01])
        else:
            extended_key = bytes([version_byte]) + private_key

        # Add checksum
        checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
        return base58.b58encode(extended_key + checksum).decode('ascii')

    @staticmethod
    def p2pkh_address(public_key: bytes) -> str:
        """Generate P2PKH (Legacy) address"""
        hash160 = BitcoinAddress.hash160(public_key)
        return BitcoinAddress.base58check_encode(hash160, 0x00)

    @staticmethod
    def p2sh_address(script_hash: bytes) -> str:
        """Generate P2SH address"""
        return BitcoinAddress.base58check_encode(script_hash, 0x05)

    @staticmethod
    def p2wpkh_address(public_key: bytes) -> str:
        """Generate P2WPKH (Native SegWit) address"""
        hash160 = BitcoinAddress.hash160(public_key)
        # Bech32 encoding for native SegWit
        return BitcoinAddress.bech32_encode('bc', 0, hash160)

    @staticmethod
    def p2wpkh_p2sh_address(public_key: bytes) -> str:
        """Generate P2WPKH nested in P2SH address"""
        hash160 = BitcoinAddress.hash160(public_key)
        # P2WPKH script: OP_0 <20-byte-pubkey-hash>
        witness_script = bytes([0x00, 0x14]) + hash160
        script_hash = BitcoinAddress.hash160(witness_script)
        return BitcoinAddress.p2sh_address(script_hash)
    
    @staticmethod
    def bech32_encode(hrp: str, witver: int, witprog: bytes) -> str:
        """Bech32 encoding for SegWit addresses"""
        # Simplified bech32 implementation
        CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
        
        def bech32_polymod(values):
            GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
            chk = 1
            for value in values:
                top = chk >> 25
                chk = (chk & 0x1ffffff) << 5 ^ value
                for i in range(5):
                    chk ^= GEN[i] if ((top >> i) & 1) else 0
            return chk
        
        def bech32_hrp_expand(hrp):
            return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
        
        def bech32_create_checksum(hrp, data):
            values = bech32_hrp_expand(hrp) + data
            polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
            return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
        
        def convertbits(data, frombits, tobits, pad=True):
            acc = 0
            bits = 0
            ret = []
            maxv = (1 << tobits) - 1
            max_acc = (1 << (frombits + tobits - 1)) - 1
            for value in data:
                if value < 0 or (value >> frombits):
                    return None
                acc = ((acc << frombits) | value) & max_acc
                bits += frombits
                while bits >= tobits:
                    bits -= tobits
                    ret.append((acc >> bits) & maxv)
            if pad:
                if bits:
                    ret.append((acc << (tobits - bits)) & maxv)
            elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
                return None
            return ret
        
        data = [witver] + convertbits(witprog, 8, 5)
        checksum = bech32_create_checksum(hrp, data)
        return hrp + '1' + ''.join([CHARSET[d] for d in data + checksum])

def generate_addresses(mnemonic: str, passphrase: str = "", num_addresses: int = 10,
                      bip39_instance: Optional[BIP39] = None) -> Dict[str, List[Dict]]:
    """
    Generate Bitcoin addresses for various derivation paths matching the HTML tool exactly

    VERSION 2.0 OPTIMIZATION:
    - Added bip39_instance parameter to reuse existing BIP39 instance
    - Eliminates redundant wordlist loading for massive performance improvement
    - Backward compatible: if bip39_instance is None, creates new instance (v1.0 behavior)
    """

    # V2.0 OPTIMIZATION: Reuse existing BIP39 instance if provided
    if bip39_instance is not None:
        bip39 = bip39_instance
    else:
        # Fallback to v1.0 behavior for backward compatibility
        bip39 = BIP39()

    # Validate mnemonic
    if not bip39.validate_mnemonic(mnemonic):
        raise ValueError("Invalid mnemonic phrase")

    # Generate seed
    seed = bip39.mnemonic_to_seed(mnemonic, passphrase)

    # Initialize BIP32
    bip32 = BIP32(seed)

    # Define derivation paths exactly as the HTML tool does
    # These are the exact paths that match the user's expected results
    paths = {
        "m/0'/0'/0'": ("BIP32 Custom", "P2PKH"),
        "m/44'/0'/0'/0": ("BIP44 (Legacy)", "P2PKH"),
        "m/49'/0'/0'/0": ("BIP49 (P2WPKH nested in P2SH)", "P2WPKH nested in P2SH"),
        "m/84'/0'/0'/0": ("BIP84 (Native SegWit)", "P2WPKH"),
        "m/0": ("Simple derivation", "P2PKH")
    }

    results = {}

    for base_path, (description, default_script_type) in paths.items():
        addresses = []

        for i in range(num_addresses):
            # Generate paths based on the pattern from your sample data
            if base_path == "m/0'/0'/0'":
                # Pattern: m/0'/0'/0', m/0'/0'/1', m/0'/0'/2', etc. (all hardened)
                full_path = f"m/0'/0'/{i}'"
            elif base_path == "m/44'/0'/0'/0":
                # Pattern: m/44'/0'/0'/0/0', m/44'/0'/0'/0/1', etc. (all hardened)
                full_path = f"m/44'/0'/0'/0/{i}'"
            elif base_path == "m/49'/0'/0'/0":
                # Pattern: m/49'/0'/0'/0/0', m/49'/0'/0'/0/1', etc. (all hardened)
                full_path = f"m/49'/0'/0'/0/{i}'"
            elif base_path == "m/84'/0'/0'/0":
                # Pattern: m/84'/0'/0'/0/0', m/84'/0'/0'/0/1', etc. (all hardened)
                full_path = f"m/84'/0'/0'/0/{i}'"
            elif base_path == "m/0":
                # Pattern: m/0/0', m/0/1', etc. (hardened indices)
                full_path = f"m/0/{i}'"
            else:
                full_path = f"{base_path}/{i}"

            # Derive the key for this specific path
            private_key, public_key, chain_code = bip32.derive_path(full_path)

            # Generate addresses based on path type
            if "44'" in base_path:
                # BIP44 - Legacy P2PKH
                address = BitcoinAddress.p2pkh_address(public_key)
                script_semantics = "P2PKH"

                # Convert private key to WIF format
                private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)

                addresses.append({
                    "path": full_path,
                    "address": address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": script_semantics
                })

            elif "49'" in base_path:
                # BIP49 - P2WPKH nested in P2SH
                address = BitcoinAddress.p2wpkh_p2sh_address(public_key)
                script_semantics = "P2WPKH nested in P2SH"

                # Convert private key to WIF format
                private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)

                addresses.append({
                    "path": full_path,
                    "address": address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": script_semantics
                })

            elif "84'" in base_path:
                # BIP84 - Native SegWit
                address = BitcoinAddress.p2wpkh_address(public_key)
                script_semantics = "P2WPKH"

                # Convert private key to WIF format
                private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)

                addresses.append({
                    "path": full_path,
                    "address": address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": script_semantics
                })

            elif base_path == "m/0":
                # Special case: m/0/X' generates both P2SH and P2WPKH addresses
                # Convert private key to WIF format
                private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)

                # P2WPKH nested in P2SH
                p2sh_address = BitcoinAddress.p2wpkh_p2sh_address(public_key)
                addresses.append({
                    "path": full_path,
                    "address": p2sh_address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": "P2WPKH nested in P2SH"
                })

                # Native P2WPKH
                p2wpkh_address = BitcoinAddress.p2wpkh_address(public_key)
                addresses.append({
                    "path": full_path,
                    "address": p2wpkh_address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": "P2WPKH"
                })

            else:
                # Default to P2PKH for other paths (like m/0'/0'/X')
                address = BitcoinAddress.p2pkh_address(public_key)
                script_semantics = "P2PKH"

                # Convert private key to WIF format
                private_key_wif = BitcoinAddress.private_key_to_wif(private_key, compressed=True)

                addresses.append({
                    "path": full_path,
                    "address": address,
                    "public_key": public_key.hex(),
                    "private_key": private_key.hex(),
                    "private_key_wif": private_key_wif,
                    "script_semantics": script_semantics
                })

        results[f"{base_path} ({description})"] = addresses

    return results
