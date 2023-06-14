from application import app
from application import auth_mid

@app.route("/")
def hello_world():
    return "<p>Welcome to the backend fool! MORE INFO TO COME<p>"

from application import api
# from application import auth_mid

# Api Endpoints

api.add_resource(auth_mid.UserRegistration, '/signup') #POST

api.add_resource(auth_mid.UserLogin, '/login') # POST

api.add_resource(auth_mid.UserLogoutAccess, '/logout/access') #POST

# api.add_resource(auth.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(auth.TokenRefresh, '/token/refresh')
# api.add_resource(auth.AllUsers, '/users')

api.add_resource(auth_mid.SecretResource, '/secret')
