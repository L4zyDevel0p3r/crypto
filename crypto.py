from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os
import sys


class Crypto:
    _crypto_extension = ".hcf"

    def __init__(self, file: str, key_file: str = None):
        file_basename = os.path.basename(file)
        name, ext = os.path.splitext(file_basename)
        self.file = file
        # File Name
        self.name = name
        # File Extension
        self.extension = ext
        self.key_file = key_file
        self._key = None

    def _generate_key(self):
        key = Fernet.generate_key()
        self._key = key

        # Saving the generated key
        with open(f"{self.name}_key.key", "wb") as key_file:
            key_file.write(key)

    def encrypt(self):
        """
        Encrypt file
        """

        try:
            # Opening file to encrypt
            with open(self.file, "rb") as file:
                original_file = file.read()
        except FileNotFoundError:
            print(f"{self.file} not found!")
            sys.exit()

        # Generating a key
        self._generate_key()
        fernet = Fernet(self._key)

        print(f"\nEncrypting {self.name}...")
        # Encrypting the file
        encrypted = fernet.encrypt(original_file)

        print(f"Saving {self.name}_encrypted{self.extension}{self._crypto_extension}...")
        # Opening the file in write mode and writing the encrypted data
        with open(f"{self.name}_encrypted{self.extension}{self._crypto_extension}", "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(
            f"{self.name} was encrypted successfully.\n\n"
            "Note:\n"
            f"1. Keep {self.name}_key.key somewhere safe!"
        )

    def decrypt(self):
        """
        Decrypt file
        """

        # Getting absolute file name. (Removing '_encrypted' part from encrypted file name.)
        absolute_name = self.name.replace("_encrypted", "")
        self.name = absolute_name

        try:
            # Opening key file and read key
            with open(f"{self.name}_key.key", "rb") as key_file:
                self._key = key_file.read()
        except FileNotFoundError:
            print(f"{self.name}_key.key not found!")
            sys.exit()

        fernet = Fernet(self._key)

        try:
            # Opening file to decrypt
            with open(f"{self.name}_encrypted{self.extension}", "rb") as file:
                encrypted_file = file.read()
        except FileNotFoundError:
            print(f"{self.name}_encrypted{self.extension} not found!")
            sys.exit()

        print(f"\nDecrypting {self.name}_encrypted{self.extension}...")

        try:
            # Decrypting the file
            decrypted = fernet.decrypt(encrypted_file)
        except InvalidToken:
            print("Key is invalid!")
            sys.exit()

        print(f"Saving {self.name}_decrypted{self.extension}...")
        # Opening the file in write mode and writing the decrypted data
        with open(f"{self.name}_decrypted{self.extension}", "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print(f"{self.name}_encrypted{self.extension} was decrypted successfully.")
