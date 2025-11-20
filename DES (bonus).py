"""
DES Encryption/Decryption Application
Combines custom DES implementation with PyCryptodome library
Supports ECB and CBC modes for educational purposes

REFERENCES AND ACKNOWLEDGMENTS:
================================
Source code adapted from: https://github.com/Vipul97/des
- Repository by Vipul97 (MIT License)
- DES implementation structure, key generation, and encryption/decryption logic
  have been combined and restructured for this educational application

EDUCATIONAL PURPOSE:
This implementation is designed for educational purposes to demonstrate
how DES encryption works internally. The code has been restructured and
combined with additional features for learning purposes.
"""

import sys
import os

try:
    from Crypto.Cipher import DES
    from Crypto.Random import get_random_bytes
    PYCRYPTODOME_AVAILABLE = True
except ImportError:
    PYCRYPTODOME_AVAILABLE = False
    print("Note: PyCryptodome not installed. Install with: pip install pycryptodome")
    print("Running with custom implementation only.\n")

# ===========================
# CUSTOM DES IMPLEMENTATION
# ===========================
# Code adapted from: https://github.com/Vipul97/des
# Restructured and combined for educational purposes

# Permutation Tables
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

SBOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]


def hex_to_bin(hex_str):
    """Convert hex string to binary string
    Utility function for hex-to-binary conversion"""
    return bin(int(hex_str, 16))[2:].zfill(64)


def bin_to_hex(bin_str):
    """Convert binary string to hex string
    Utility function for binary-to-hex conversion"""
    return hex(int(bin_str, 2))[2:].upper().zfill(16)


def permute(bits, table):
    """Apply permutation table to bits
    Core permutation operation used throughout DES
    Adapted from: https://github.com/Vipul97/des"""
    return ''.join(bits[i - 1] for i in table)


def xor(a, b):
    """XOR two binary strings
    Fundamental operation in DES encryption"""
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))


def left_shift(bits, n):
    """Circular left shift"""
    return bits[n:] + bits[:n]


def sbox_substitution(bits):
    """Apply S-box substitution"""
    output = ''
    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        val = SBOX[i][row][col]
        output += bin(val)[2:].zfill(4)
    return output


def generate_round_keys(key_bin):
    """Generate 16 round keys from the main key
    Key schedule algorithm adapted from: https://github.com/Vipul97/des
    Implements PC1 permutation, key splitting, and left shifts"""
    keys = []
    key_56 = permute(key_bin, PC1)
    C, D = key_56[:28], key_56[28:]
    
    for shift in SHIFT:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        keys.append(permute(C + D, PC2))
    
    return keys


def feistel_function(R, K):
    """The Feistel (F) function
    Core transformation function in DES
    Implementation adapted from: https://github.com/Vipul97/des"""
    expanded = permute(R, E)
    xored = xor(expanded, K)
    substituted = sbox_substitution(xored)
    return permute(substituted, P)


def des_process(data_bin, keys, encrypt=True):
    """Core DES processing (encryption or decryption)
    Main DES algorithm implementation
    Structure adapted from: https://github.com/Vipul97/des"""
    if not encrypt:
        keys = keys[::-1]  # Reverse keys for decryption
    
    data = permute(data_bin, IP)
    L, R = data[:32], data[32:]
    
    for key in keys:
        new_R = xor(L, feistel_function(R, key))
        L, R = R, new_R
    
    return permute(R + L, FP)  # Note: R + L (swap)


class CustomDES:
    """Custom DES implementation"""
    
    @staticmethod
    def encrypt_ecb(plaintext_hex, key_hex):
        """Encrypt using ECB mode"""
        plaintext_bin = hex_to_bin(plaintext_hex)
        key_bin = hex_to_bin(key_hex)
        keys = generate_round_keys(key_bin)
        ciphertext_bin = des_process(plaintext_bin, keys, encrypt=True)
        return bin_to_hex(ciphertext_bin)
    
    @staticmethod
    def decrypt_ecb(ciphertext_hex, key_hex):
        """Decrypt using ECB mode"""
        ciphertext_bin = hex_to_bin(ciphertext_hex)
        key_bin = hex_to_bin(key_hex)
        keys = generate_round_keys(key_bin)
        plaintext_bin = des_process(ciphertext_bin, keys, encrypt=False)
        return bin_to_hex(plaintext_bin)
    
    @staticmethod
    def encrypt_cbc(plaintext_hex, key_hex, iv_hex):
        """Encrypt using CBC mode"""
        plaintext_bin = hex_to_bin(plaintext_hex)
        key_bin = hex_to_bin(key_hex)
        iv_bin = hex_to_bin(iv_hex)
        keys = generate_round_keys(key_bin)
        
        # XOR plaintext with IV before encryption
        xored = xor(plaintext_bin, iv_bin)
        ciphertext_bin = des_process(xored, keys, encrypt=True)
        return bin_to_hex(ciphertext_bin)
    
    @staticmethod
    def decrypt_cbc(ciphertext_hex, key_hex, iv_hex):
        """Decrypt using CBC mode"""
        ciphertext_bin = hex_to_bin(ciphertext_hex)
        key_bin = hex_to_bin(key_hex)
        iv_bin = hex_to_bin(iv_hex)
        keys = generate_round_keys(key_bin)
        
        # Decrypt then XOR with IV
        decrypted_bin = des_process(ciphertext_bin, keys, encrypt=False)
        plaintext_bin = xor(decrypted_bin, iv_bin)
        return bin_to_hex(plaintext_bin)


# ===========================
# PYCRYPTODOME WRAPPER
# ===========================

class PyCryptoDES:
    """PyCryptodome DES wrapper for comparison"""
    
    @staticmethod
    def encrypt_ecb(plaintext_hex, key_hex):
        """Encrypt using PyCryptodome ECB mode"""
        if not PYCRYPTODOME_AVAILABLE:
            return None
        
        key = bytes.fromhex(key_hex)
        plaintext = bytes.fromhex(plaintext_hex)
        cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext.hex().upper()
    
    @staticmethod
    def decrypt_ecb(ciphertext_hex, key_hex):
        """Decrypt using PyCryptodome ECB mode"""
        if not PYCRYPTODOME_AVAILABLE:
            return None
        
        key = bytes.fromhex(key_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.hex().upper()
    
    @staticmethod
    def encrypt_cbc(plaintext_hex, key_hex, iv_hex):
        """Encrypt using PyCryptodome CBC mode"""
        if not PYCRYPTODOME_AVAILABLE:
            return None
        
        key = bytes.fromhex(key_hex)
        plaintext = bytes.fromhex(plaintext_hex)
        iv = bytes.fromhex(iv_hex)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext.hex().upper()
    
    @staticmethod
    def decrypt_cbc(ciphertext_hex, key_hex, iv_hex):
        """Decrypt using PyCryptodome CBC mode"""
        if not PYCRYPTODOME_AVAILABLE:
            return None
        
        key = bytes.fromhex(key_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)
        iv = bytes.fromhex(iv_hex)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.hex().upper()


# ===========================
# USER INTERFACE
# ===========================

def validate_hex(hex_str, length):
    """Validate hexadecimal string"""
    if len(hex_str) != length:
        return False
    try:
        int(hex_str, 16)
        return True
    except ValueError:
        return False


def print_header():
    """Print application header"""
    print("=" * 70)
    print("DES ENCRYPTION/DECRYPTION TOOL".center(70))
    print("Custom Implementation + PyCryptodome Library".center(70))
    print("=" * 70)
    print()


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 70)
    print("MAIN MENU")
    print("=" * 70)
    print("1. ECB Mode - Electronic Codebook")
    print("2. CBC Mode - Cipher Block Chaining")
    print("3. Compare Custom vs PyCryptodome")
    print("4. Batch Test Mode")
    print("5. Exit")
    print("=" * 70)


def ecb_mode():
    """ECB mode encryption/decryption"""
    print("\n" + "-" * 70)
    print("ECB MODE - Electronic Codebook")
    print("-" * 70)
    
    # Get inputs
    while True:
        key = input("Enter 64-bit key (16 hex digits): ").strip().upper()
        if validate_hex(key, 16):
            break
        print("❌ Invalid! Must be 16 hexadecimal characters.")
    
    while True:
        plaintext = input("Enter 64-bit plaintext (16 hex digits): ").strip().upper()
        if validate_hex(plaintext, 16):
            break
        print("❌ Invalid! Must be 16 hexadecimal characters.")
    
    # Custom implementation
    print("\n🔧 CUSTOM IMPLEMENTATION:")
    print("-" * 70)
    ciphertext_custom = CustomDES.encrypt_ecb(plaintext, key)
    print(f"Ciphertext:  {ciphertext_custom}")
    
    decrypted_custom = CustomDES.decrypt_ecb(ciphertext_custom, key)
    print(f"Decrypted:   {decrypted_custom}")
    print(f"Verified:    {'✅ PASS' if decrypted_custom == plaintext else '❌ FAIL'}")
    
    # PyCryptodome comparison
    if PYCRYPTODOME_AVAILABLE:
        print("\n📚 PYCRYPTODOME LIBRARY:")
        print("-" * 70)
        ciphertext_lib = PyCryptoDES.encrypt_ecb(plaintext, key)
        print(f"Ciphertext:  {ciphertext_lib}")
        
        decrypted_lib = PyCryptoDES.decrypt_ecb(ciphertext_lib, key)
        print(f"Decrypted:   {decrypted_lib}")
        print(f"Verified:    {'✅ PASS' if decrypted_lib == plaintext else '❌ FAIL'}")
        
        print("\n🔍 COMPARISON:")
        print("-" * 70)
        print(f"Match:       {'✅ IDENTICAL' if ciphertext_custom == ciphertext_lib else '❌ DIFFERENT'}")


def cbc_mode():
    """CBC mode encryption/decryption"""
    print("\n" + "-" * 70)
    print("CBC MODE - Cipher Block Chaining")
    print("-" * 70)
    
    # Get inputs
    while True:
        key = input("Enter 64-bit key (16 hex digits): ").strip().upper()
        if validate_hex(key, 16):
            break
        print("❌ Invalid! Must be 16 hexadecimal characters.")
    
    while True:
        plaintext = input("Enter 64-bit plaintext (16 hex digits): ").strip().upper()
        if validate_hex(plaintext, 16):
            break
        print("❌ Invalid! Must be 16 hexadecimal characters.")
    
    while True:
        iv = input("Enter 64-bit IV (16 hex digits): ").strip().upper()
        if validate_hex(iv, 16):
            break
        print("❌ Invalid! Must be 16 hexadecimal characters.")
    
    # Custom implementation
    print("\n🔧 CUSTOM IMPLEMENTATION:")
    print("-" * 70)
    ciphertext_custom = CustomDES.encrypt_cbc(plaintext, key, iv)
    print(f"Ciphertext:  {ciphertext_custom}")
    
    decrypted_custom = CustomDES.decrypt_cbc(ciphertext_custom, key, iv)
    print(f"Decrypted:   {decrypted_custom}")
    print(f"Verified:    {'✅ PASS' if decrypted_custom == plaintext else '❌ FAIL'}")
    
    # PyCryptodome comparison
    if PYCRYPTODOME_AVAILABLE:
        print("\n📚 PYCRYPTODOME LIBRARY:")
        print("-" * 70)
        ciphertext_lib = PyCryptoDES.encrypt_cbc(plaintext, key, iv)
        print(f"Ciphertext:  {ciphertext_lib}")
        
        decrypted_lib = PyCryptoDES.decrypt_cbc(ciphertext_lib, key, iv)
        print(f"Decrypted:   {decrypted_lib}")
        print(f"Verified:    {'✅ PASS' if decrypted_lib == plaintext else '❌ FAIL'}")
        
        print("\n🔍 COMPARISON:")
        print("-" * 70)
        print(f"Match:       {'✅ IDENTICAL' if ciphertext_custom == ciphertext_lib else '❌ DIFFERENT'}")


def batch_test():
    """Run batch tests with predefined test vectors"""
    print("\n" + "-" * 70)
    print("BATCH TEST MODE")
    print("-" * 70)
    
    test_vectors = [
        {"key": "133457799BBCDFF1", "plaintext": "0123456789ABCDEF", "name": "Test 1"},
        {"key": "AABB09182736CCDD", "plaintext": "123456ABCD132536", "name": "Test 2"},
        {"key": "0E329232EA6D0D73", "plaintext": "8787878787878787", "name": "Test 3"},
    ]
    
    print(f"\nRunning {len(test_vectors)} test vectors...\n")
    
    for i, test in enumerate(test_vectors, 1):
        print(f"{test['name']}:")
        print(f"  Key:       {test['key']}")
        print(f"  Plaintext: {test['plaintext']}")
        
        cipher = CustomDES.encrypt_ecb(test['plaintext'], test['key'])
        decrypted = CustomDES.decrypt_ecb(cipher, test['key'])
        
        print(f"  Cipher:    {cipher}")
        print(f"  Decrypted: {decrypted}")
        print(f"  Status:    {'✅ PASS' if decrypted == test['plaintext'] else '❌ FAIL'}")
        print()


def main():
    """Main application loop"""
    print_header()
    
    print("📖 Welcome to the DES Encryption/Decryption Tool!")
    print("\nThis tool combines:")
    print("  • Custom DES implementation (educational)")
    print("  • PyCryptodome library (production-ready)")
    print("\nSupported modes: ECB, CBC")
    print("Input format: 16 hexadecimal digits (64 bits)")
    
    while True:
        print_menu()
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            ecb_mode()
        elif choice == '2':
            cbc_mode()
        elif choice == '3':
            print("\n🔍 Running comparison test...")
            ecb_mode()
        elif choice == '4':
            batch_test()
        elif choice == '5':
            print("\n👋 Thank you for using DES Encryption Tool!")
            print("=" * 70)
            break
        else:
            print("\n❌ Invalid choice! Please select 1-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()