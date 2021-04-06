from cryptography.fernet import Fernet
import os


class Crypto:
    _FileName = None
    _FileExtension = None

    def __init__(self, file: str):
        name, ext = os.path.splitext(file)
        self._FileName = name
        self._FileExtension = ext
