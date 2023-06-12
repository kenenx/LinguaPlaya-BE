from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

CORS(app)

# app.config['SECRET_KEY'] = '20172ef817c8b8e9f34067ef3f5b2b5c'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ornaazhm:dlgrUjmXKiyiQFOdjkqg2U1j6xUOFLh2@lucky.db.elephantsql.com/ornaazhm'

db=SQLAlchemy(app)

from application import routes
from application import models

if __name__ == '__main__':
    app.run()