from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from pathlib import Path
import os
import sys


class Crypto:
    _crypto_extension = ".hcf"
    # Save encrypted files here
    _encrypted_files = "/encrypted/"
    # Save decrypted files here
    _decrypted_files = "/decrypted/"
    # Save key files here
    _key_files = "/keys/"

    def __init__(self, file: str):
        self.file_basename = os.path.basename(file)
        name, ext = os.path.splitext(self.file_basename)
        self.file = file
        # File Name
        self.name = name
        # File Extension
        self.extension = ext
        self._key = None

    @classmethod
    def make_dir(cls, path: str) -> None:
        """
        Create a new directory at this given path.
        """
        if not os.path.exists(path):
            p = Path(path)
            p.mkdir(exist_ok=True)

    def _generate_key(self):
        key = Fernet.generate_key()
        self._key = key

        # Creating a folder inside _key_files folder with file name
        dirname = f"{self._key_files}{self.name}/"
        self.make_dir(path=dirname)

        # Saving the generated key
        with open(f"{dirname}{self.name}.key", "wb") as key_file:
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

        # Creating a folder inside _encrypted_files folder with file name
        dirname = f"{self._encrypted_files}{self.name}/"
        self.make_dir(path=dirname)

        print(f"\nEncrypting {self.name}{self.extension} ...")
        # Encrypting the file
        encrypted = fernet.encrypt(original_file)
        encrypted_filename = f"{self.name}{self.extension}{self._crypto_extension}"

        # Opening the file in write mode and writing the encrypted data
        print(f"Saving {encrypted_filename} ...")
        with open(f"{dirname}{encrypted_filename}", "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(
            f"{self.name}{self.extension} was encrypted successfully.\n\n"
            f"{encrypted_filename} was saved on {dirname}\n"
            "Note:\n"
            f"1. Keep {self.name}.key somewhere safe!"
        )

    def decrypt(self, key_file: str):
        """
        Decrypt file
        """

        try:
            # Opening file to decrypt
            with open(f"{self.file}", "rb") as file:
                encrypted_file = file.read()
        except FileNotFoundError:
            print(f"{self.file} not found!")
            sys.exit()

        try:
            # Opening key file and read key
            with open(f"{key_file}", "rb") as file:
                self._key = file.read()
        except FileNotFoundError:
            print(f"{key_file} not found!")
            sys.exit()

        fernet = Fernet(self._key)

        print(f"\nDecrypting {self.file_basename} ...")

        try:
            # Decrypting the file
            decrypted = fernet.decrypt(encrypted_file)
        except InvalidToken:
            print("Key is invalid!")
            sys.exit()

        # Removing _crypto_extension from file name
        removed_extension = self.file_basename.replace(self._crypto_extension, "")
        self.name, self.extension = os.path.splitext(removed_extension)
        decrypted_filename = f"{self.name}_decrypted{self.extension}"

        # Creating a folder inside _decrypted_files folder with file name
        dirname = f"{self._decrypted_files}{self.name}/"
        self.make_dir(path=dirname)

        print(f"Saving {decrypted_filename} ...")
        # Opening the file in write mode and writing the decrypted data
        with open(f"{dirname}{decrypted_filename}", "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print(
            f"{self.file_basename} was decrypted successfully.\n"
            f"{decrypted_filename} was saved on {dirname}"
        )
