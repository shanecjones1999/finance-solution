from utils.CryptographyUtils import CryptographyUtils
# from database.data.LoginData import LoginData
from database.Connection import Session, User
# from database.Models.User import User
from datetime import datetime


class LoginLogic:
    def __init__(self):
        self.session = Session()
        # self.loginData = LoginData()

    def are_valid_credentials(self, username: str, password: str):
        user = self.session.query(User).filter(
            User.username == username).first()

        if not user:
            return False
        hashed_password = CryptographyUtils.encrypt(password)

        # real_hashed_password = self.get_hashed_password(username)
        return hashed_password == user.password

    # def get_hashed_password(self, username: str):
    #     return self.loginData.get_encrypted_password(username)

    def handle_registration(self, username: str, password: str):
        if self.is_username_available(username):
            new_user = User(
                username=username,
                password=CryptographyUtils.encrypt(password),
                created_at_utc=datetime.utcnow(),
                updated_at_utc=datetime.utcnow()
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        else:
            return False

        # if not self.loginData.is_username_available(username):
        #     return False, "Username is not available."

        # hashed_password = CryptographyUtils.encrypt(password)
        # self.loginData.create_user(username, hashed_password)
        # return True, ""

    def is_username_available(self, username):
        existing_user = self.session.query(User).filter(
            User.username == username).first()
        return existing_user is None
