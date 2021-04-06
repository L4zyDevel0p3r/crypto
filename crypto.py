from cryptography.fernet import Fernet
import os


class Crypto:

    def __init__(self, file: str):
        name, ext = os.path.splitext(file)
        self.file_name = name
        self.file_extension = ext
        self._key = None

    def _generate_key(self):
        key = Fernet.generate_key()
        self._key = key
