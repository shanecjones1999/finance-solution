import hashlib


class PasswordUtils:
    @staticmethod
    def encrypt_password(password: str):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password
