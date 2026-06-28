# # Principle: Functionality over purity: If it works, keep it.
# # We don't care how it works or what "dark magic" it uses.
# # It's chaos and madness, and we love it. The more chaos, the more fun.
# # Users can fuck off and do whatever they want, we don't wipe their asses.
# # Let them have fun, screw up, if they forget their password, they'll lose their life, and if they remember, they'll restore
# # only what they managed to sync, and fuck off with questions.
# # This file marks the 'modules' directory as a Python package.
# # It can be left empty for simple package initialization.
# # For more complex packages, it might contain imports,
# # package-level variables, or functions to be exposed.
# # i don't care what you think just use the biggest dildos you know to make everyone happy
# # I don't care how they work as long as they work

# This is the rocket fuel that you and I will use to put out fires.

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
import base64

class CryptoUtils:
    """
    Conceptual utility class for basic file encryption/decryption using Fernet.
    In a real-world scenario, key management and security would be significantly
    more complex and robust.

    Note: This is FOR DEMONSTRATION PURPOSES ONLY and NOT suitable for
    production environments with sensitive data.
    """
    def __init__(self, master_key: str):
        # In a real app, master_key would be derived from user's strong password
        # or managed by a secure key management system.
        # For this demo, we'll just use it directly.
        if not isinstance(master_key, str) or not master_key:
            raise ValueError("Master key must be a non-empty string.")

        # Derive a consistent Fernet key from the master_key for this conceptual demo
        # using a fixed salt for simplicity, but real apps should use unique salts.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'fixed_salt_for_demo_only', # !!! FOR DEMO ONLY, USE UNIQUE SALT IN REAL APPS !!!
            iterations=100000, # A reasonable number of iterations for a demo
        )
        self.fernet_key = urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.fernet = Fernet(self.fernet_key)

    def _derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Derives a key from a password and salt using PBKDF2HMAC.
        This is a helper for encryption of individual files, distinct from the master_key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000, # Higher iterations for password-based encryption
        )
        return urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_data(self, data_bytes: bytes, password: str) -> bytes:
        """Encrypts data bytes with a password, including a salt."""
        salt = os.urandom(16)
        key = self._derive_key_from_password(password, salt)
        f = Fernet(key)
        encrypted_data = f.encrypt(data_bytes)
        return salt + encrypted_data # Prepend salt to encrypted data

    def decrypt_data(self, encrypted_data_with_salt: bytes, password: str) -> bytes | None:
        """Decrypts data bytes with a password, assuming salt is prepended."""
        if len(encrypted_data_with_salt) < 16:
            print("Decryption Error: Data too short, missing salt.")
            return None

        salt = encrypted_data_with_salt[:16]
        encrypted_data = encrypted_data_with_salt[16:]

        try:
            key = self._derive_key_from_password(password, salt)
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            print(f"Decryption Error: Incorrect password or corrupted data: {e}")
            return None


    def encrypt_file(self, input_filepath: str, output_filepath: str):
        """
        Conceptually encrypts a file.
        Uses the instance's fernet_key for simplicity (as if it's the master key).
        In a real app, this would be more nuanced, possibly using different keys.
        """
        try:
            with open(input_filepath, 'rb') as f:
                plaintext = f.read()

            encrypted_data = self.fernet.encrypt(plaintext)

            with open(output_filepath, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Encryption failed for {input_filepath}: {e}")
            return False

    def decrypt_file(self, input_filepath: str, output_filepath: str):
        """
        Conceptually decrypts a file.
        Uses the instance's fernet_key.
        """
        try:
            with open(input_filepath, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = self.fernet.decrypt(encrypted_data)

            with open(output_filepath, 'wb') as f:
                f.write(decrypted_data)
            return True
        except Exception as e:
            print(f"Decryption failed for {input_filepath}: {e}")
            return False

    def hash_password(self, password: str) -> str:
        """
        Hashes a password conceptually.
        In a real app, use libraries like `passlib` with strong algorithms (e.g., bcrypt, Argon2).
        """
        # This is a very basic conceptual hash. DO NOT USE IN PRODUCTION.
        # A real hash would involve a salt and a strong, slow hashing algorithm.
        return base64.b64encode(self.fernet_key + password.encode()).decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Conceptually verifies a password against a hash.
        """
        # This is a very basic conceptual verification. DO NOT USE IN PRODUCTION.
        return self.hash_password(password) == hashed_password

