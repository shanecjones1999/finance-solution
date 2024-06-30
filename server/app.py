from flask import Flask
from flask_cors import CORS
from config import Config
from database.Database import Database

from controllers.LoginController import login_blueprint
from controllers.LinkController import link_blueprint


app = Flask(__name__)
CORS(app, resources={
     r"*": {"origins": "*"}}, supports_credentials=True)

app.config.from_object(Config)

app.register_blueprint(login_blueprint)
app.register_blueprint(link_blueprint)

Database.initialize()


if __name__ == '__main__':
    app.run(debug=True)
