from application import app, db
from application import routes
# from application.models import Pokemon
from flask import request
from flask import jsonify
from flask import render_template
# from application.forms import AddPokemon

@app.route("/")
def hello_world():
    return "<p>Hello, there!<p>"