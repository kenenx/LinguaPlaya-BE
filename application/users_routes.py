from application import app, db
from application import users_routes
from application.models import Users
from flask import request
from flask import jsonify

@app.route("/")
def hello_world():
    return "<p>Welcome to the backend fool!<p>"


#creat user
# @app.route("/users",methods = "[POST]")
# def create_user():
    
#     user = Users() 
#     db.session.add(user)
#     db.session.commit()
#     # data = request.json
#     return jsonify(id = user.users_id, name =user.name,email = user.email, password = user.password )

def format_users(user):
    return {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }

# get user
@app.route('/users/<id>', methods=['GET'])
def get_character(id):
    user = Users.query.filter_by(users_id=id).first()
    #getuser = format_users(user) 
    return  jsonify(id = user.users_id, name =user.name,age = user.age,email = user.email)



# delete user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
  user = Users.query.filter_by(users_id=id).first()
  db.session.delete(user)
  db.session.commit()
  return 'User successfully deleted'

# update users 
app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    user = Users.query.filter_by(users_id=id).first()
    if not user:
        return jsonify({'error': 'User not found'})

    data = request.json
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.email = data.get('email', user.email)
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.rating = data.get('rating', user.rating)
    user.flags = data.get('rating', user.flags)
    user.connections = data.get('rating', user.connections)
    user.time_zone = data.get('rating', user.time_zone)
    user.last_online = data.get('rating', user.last_online)

    db.session.commit()

    updatedUser = Users.query.get(id)
    return jsonify(id=updatedUser.users_id, name=updatedUser.name, age=updatedUser.age, email=updatedUser.email)
