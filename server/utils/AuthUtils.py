import jwt
from config import Config


class AuthUtils:

    @staticmethod
    def generate_token(username):
        algorithm = 'HS256'
        payload = {}
        payload['username'] = username
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm)
        return token
