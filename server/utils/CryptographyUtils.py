import hashlib


class CryptographyUtils:
    @staticmethod
    def encrypt(string: str):
        hashed_string = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return hashed_string
