import jwt
from config import Config


class AuthUtils:

    @staticmethod
    def generate_token(user_id):
        algorithm = 'HS256'
        payload = {}
        payload['userId'] = user_id
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm)
        return token

    @staticmethod
    def decode_token(token):
        algorithm = 'HS256'
        try:
            decoded_payload = jwt.decode(token, Config.SECRET_KEY, algorithm)
            return decoded_payload['userId']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def decode_request_auth(request):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1]
            user_id = AuthUtils.decode_token(token)
            return user_id
        except:
            return None
