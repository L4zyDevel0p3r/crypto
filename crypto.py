from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from pathlib import Path
import os
import sys


class Crypto:
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent

    _crypto_extension = ".hcf"
    # Save encrypted files here
    _encrypted_files = "encrypted"
    # Save decrypted files here
    _decrypted_files = "decrypted"
    # Save key files here
    _key_files = "keys"

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

        p = Path(cls.BASE_DIR, path)

        if not os.path.exists(p):
            p.mkdir(parents=True, exist_ok=True)

    def _generate_key(self):
        key = Fernet.generate_key()
        self._key = key

        # Creating a folder inside _key_files folder with file name
        dirname = os.path.join(self._key_files, self.name)
        self.make_dir(path=dirname)

        # Key file full path
        p = os.path.join(self.BASE_DIR, dirname, f"{self.name}.key")

        # Saving the generated key
        with open(p, "wb") as key_file:
            key_file.write(key)

        print(f"\n{self.name}.key was saved on {dirname}")

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
        dirname = os.path.join(self._encrypted_files, self.name)
        self.make_dir(path=dirname)

        print(f"\nEncrypting {self.name}{self.extension} ...")
        # Encrypting the file
        encrypted = fernet.encrypt(original_file)
        encrypted_filename = f"{self.name}{self.extension}{self._crypto_extension}"

        # Encrypted file full path
        p = os.path.join(self.BASE_DIR, dirname, encrypted_filename)

        # Opening the file in write mode and writing the encrypted data
        print(f"Saving {encrypted_filename} ...")
        with open(p, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        print(
            f"\n{self.name}{self.extension} was encrypted successfully!\n"
            f"{encrypted_filename} was saved on {dirname}\n\n"
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
        dirname = os.path.join(self._decrypted_files, self.name)
        self.make_dir(path=dirname)

        # Decrypted file full path
        p = os.path.join(self.BASE_DIR, dirname, decrypted_filename)

        print(f"Saving {decrypted_filename} ...")
        # Opening the file in write mode and writing the decrypted data
        with open(p, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print(
            f"\n{self.file_basename} was decrypted successfully!\n"
            f"{decrypted_filename} was saved on {dirname}"
        )
