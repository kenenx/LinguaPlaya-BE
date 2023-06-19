import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
load_dotenv()
# Making Flask Application
app = Flask(__name__)
# Object of Api class
api = Api(app)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Application Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('HUSH_HUSH')
app.config['JWT_SECRET_KEY'] = os.getenv("TOKEN_HUSH")
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# SqlAlchemy object
db = SQLAlchemy(app)

# JwtManager object
jwt = JWTManager(app)

from application.models.users_models import RevokedTokenModel

# Checking that token is in blacklist or not
# @jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(decrypted_token):

#     jti = decrypted_token['jti']

#     return RevokedTokenModel.is_jti_blacklisted(jti)

from application import routes
from application import models
# if __name__ == '__main__':
#     api.run(debug = True)
