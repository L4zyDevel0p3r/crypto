from cryptography.fernet import Fernet
import os
import sys


class Crypto:

    def __init__(self, file: str):
        name, ext = os.path.splitext(file)
        self.file = file
        # File Name
        self.name = name
        # File Extension
        self.extension = ext
        self._key = None

    def _generate_key(self):
        key = Fernet.generate_key()
        self._key = key

        # Saving the generated key
        with open(f"{self.name}_key.key", "wb") as file_key:
            file_key.write(key)

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

        print(f"\nEncrypting {self.file}...")
        # Encrypting the file
        encrypted = fernet.encrypt(original_file)

        print(f"Saving {self.name}_encrypted{self.extension}...")
        # Opening the file in write mode and writing the encrypted data
        with open(f"{self.name}_encrypted{self.extension}", "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(
            f"{self.file} was encrypted successfully.\n\n"
            "Note:\n"
            f"1. Keep {self.name}_key.key somewhere safe!\n"
            f"2. Don't rename {self.name}_encrypted{self.extension} and {self.name}_key.key"
        )

    def decrypt(self):
        """
        Decrypt file
        """

        # Getting absolute file name. (Removing '_encrypted' part from encrypted file name.)
        split_name = self.name.split("_")
        self.name = split_name[0]

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

        # Decrypting the file
        decrypted = fernet.decrypt(encrypted_file)

        # Opening the file in write mode and writing the decrypted data
        with open(f"{self.name}_decrypted{self.extension}", "wb") as decrypted_file:
            decrypted_file.write(decrypted)
