"""
A program to encrypt and decrypt data stored in vaults
"""

import os
import sys

try:
    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
except ImportError:
    print(
        "cryptography package is required to run the program.\n"
        "Kindly run `pip install cryptography` before starting me.\n"
    )
    sys.exit(0)

if os.name == "nt":
    SLASH = "\\"
else:
    SLASH = "/"
