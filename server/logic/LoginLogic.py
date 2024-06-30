from utils.CryptographyUtils import CryptographyUtils
from database.data.LoginData import LoginData


class LoginLogic:
    def __init__(self):
        self.loginData = LoginData()

    def are_valid_credentials(self, username: str, password: str):
        hashed_password = CryptographyUtils.encrypt(password)
        real_hashed_password = self.get_hashed_password(username)
        return hashed_password == real_hashed_password

    def get_hashed_password(self, username: str):
        return self.loginData.get_encrypted_password(username)

    def handle_registration(self, username: str, password: str):
        if not self.loginData.is_username_available(username):
            return False, "Username is not available."

        hashed_password = CryptographyUtils.encrypt(password)
        self.loginData.create_user(username, hashed_password)
        return True, ""
