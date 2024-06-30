from flask import Blueprint, request, jsonify, session
from flask.views import MethodView
from logic.LoginLogic import LoginLogic
from utils.AuthUtils import AuthUtils


class LoginController(MethodView):
    def __init__(self):
        self.logic = LoginLogic()

    def post(self):
        # Determine the action based on the path
        if request.path == '/api/login' or request.path == 'token':
            return self.login()
        elif request.path == '/api/register':
            return self.register()

    def get(self):
        # Determine the action based on the path
        if request.path == '/api/user_info':
            return self.user_info()
        elif request.path == '/api/user_list':
            return self.user_list()

    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if (self.logic.are_valid_credentials(username, password)):
            token = AuthUtils.generate_token(username)
            session['username'] = username
            return jsonify({"token": token}), 200

        return jsonify({"message": "Login failed"}), 401

    def register(self):
        username = request.json.get('username')
        password = request.json.get('password')

        success, error = self.logic.handle_registration(username, password)

        if not success:
            return jsonify({"message": error, "username": username}), 409

        # Add your registration logic here
        return jsonify({"message": "Registration successful", "username": username}), 200

    def user_info(self):
        user_id = request.args.get('user_id')
        # Add your user info retrieval logic here
        return jsonify({"message": "User info retrieved", "user_id": user_id}), 200

    def user_list(self):
        # Add your user list retrieval logic here
        return jsonify({"message": "User list retrieved"}), 200


login_blueprint = Blueprint('login', __name__)

login_blueprint.add_url_rule(
    '/api/login', view_func=LoginController.as_view('login'), methods=['POST'])
login_blueprint.add_url_rule(
    '/api/register', view_func=LoginController.as_view('register'), methods=['POST'])
login_blueprint.add_url_rule(
    '/api/user_info', view_func=LoginController.as_view('user_info'), methods=['GET'])
login_blueprint.add_url_rule(
    '/api/user_list', view_func=LoginController.as_view('user_list'), methods=['GET'])
