from cryptography.fernet import Fernet
import os


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

    def encrypt(self):
        """
        Encrypt file
        """

        # Generating a key
        self._generate_key()
        fernet = Fernet(self._key)

        # Opening file to encrypt
        with open(self.file, "rb") as file:
            original_file = file.read()

        # Encrypting the file
        encrypted = fernet.encrypt(original_file)

        # Opening the file in write mode and writing the encrypted data
        with open(f"{self.name}_encrypted{self.extension}", "wb") as encrypted_file:
            encrypted_file.write(encrypted)
