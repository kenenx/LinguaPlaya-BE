from application import app
from application import controller

@app.route("/")
def hello_world():
    return "<p>Welcome to the backend fool! MORE INFO TO COME<p>"

from application import api
# from application import auth_mid

# Api Endpoints

api.add_resource(controller.UserRegistration, '/signup') #POST

api.add_resource(controller.UserLogin, '/login') # POST

api.add_resource(controller.UserLogoutAccess, '/logout/access') #POST

# api.add_resource(auth.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(auth.TokenRefresh, '/token/refresh')
api.add_resource(controller.UsersDeets, '/users')

############################################################
# user
api.add_resource(controller.AllUsers, '/users/all')
api.add_resource(controller.UsersFlags, '/users/flags')
api.add_resource(controller.UsersRating, '/users/rating')

# Langauges
api.add_resource(controller.Languages,'/languages')
api.add_resource(controller.AllLanguages, '/languages/all')

# Games
api.add_resource(controller.AllGames, '/games/all')
api.add_resource(controller.Games, '/games/')
api.add_resource(controller.UserGames, '/games/<username>')
