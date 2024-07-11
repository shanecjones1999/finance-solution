from flask import request, jsonify
from functools import wraps
from utils.AuthUtils import AuthUtils


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = AuthUtils.decode_request_auth(request=request)
        if not user_id:
            return jsonify({"message": "Authentication is required"}), 401
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)

    return decorated_function
