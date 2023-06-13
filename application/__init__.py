import os

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)

app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI']

bcrypt = Bcrypt(app)
db=SQLAlchemy(app)

from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from application import users_routes
from application import models

if __name__ == '__main__':
    app.run()
