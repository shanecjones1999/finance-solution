from flask import Flask, request, session, jsonify
from flask_cors import CORS
from config import Config
from database.Database import Database

from controllers.LoginController import login_blueprint


app = Flask(__name__)
CORS(app, resources={
     r"*": {"origins": "*"}}, supports_credentials=True)

app.config.from_object(Config)

app.register_blueprint(login_blueprint)

Database.initialize()


if __name__ == '__main__':
    app.run(debug=True)
