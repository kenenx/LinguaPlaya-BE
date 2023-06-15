from flask_restful import Resource, reqparse
from flask import session
import json
from application import app,db
from application.models.users_models import UserModel, RevokedTokenModel

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

import pdb


parser = reqparse.RequestParser()

parser.add_argument('username', help='username cannot be blank', required=True)
parser.add_argument('password', help='password cannot be blank', required=True)

class UserRegistration(Resource):
    """
    User Registration Api
    """
   
    def post(self):
        parser.add_argument('email', help='email cannot be blank', required=True)
        parser.add_argument('name', help='name cannot be blank', required=True)
        data = parser.parse_args()

        username = data['username']
        name = data['name']
        email = data['email']
        # Checking that user is already exist or not
        if UserModel.find_by_username(username):

            return {'message': f'User {username} already exists'}

        # create new user
        new_user = UserModel(

            username=username,
            name= name,
            email = email,
            password=UserModel.generate_hash(data['password'])

        )
        try:
            
            # Saving user in DB and Generating Access and Refresh token
            new_user.save_to_db()
            
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            return {
            
                'message': f'User {username} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            
            }
        
        except (RuntimeError, TypeError, NameError, ValueError):
        
            return RuntimeError, TypeError, NameError, ValueError


class UserLogin(Resource):
    """
    User Login Api
    """

    def post(self):

        data = parser.parse_args()
        username = data['username']
        # Searching user by username
        current_user = UserModel.find_by_username(username)
        
        # user does not exists
        if not current_user:
        
            return {'message': f'User {username} doesn\'t exist'}
        
        # user exists, comparing password and hash
        if UserModel.verify_hash(data['password'], current_user.password):
            
            # generating access token and refresh token
            access_token = create_access_token(identity=username)
        
            refresh_token = create_refresh_token(identity=username)
        
            return {
        
                'message': f'Logged in as {username}',
                'access_token': access_token,
                'refresh_token': refresh_token
        
            }
        
        else:
        
            return {'message': "Wrong credentials"}


class UserLogoutAccess(Resource):
    """
    User Logout Api 
    """
    
    @jwt_required
    def post(self):

        jti = get_jwt()['jti']
        print('itwork?',jti)
        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)
    
            revoked_token.add()
    
    	    # if 'username' in session:
		    #     session.pop('username', None)
	        #     return jsonify({'message' : 'You successfully logged out'})
            return {'message': 'Access token has been revoked'}
    
        except:
    
            return {'message': 'Something went wrong'}, 500


#  class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api 
    """
    # @jwt_refresh_token_required
    # def post(self):

        # jti = get_jwt()['jti']
        
        # try:
        
        #     revoked_token = RevokedTokenModel(jti=jti)
        
        #     revoked_token.add()
        
        #     pdb.set_trace()
        
        #     return {'message': 'Refresh token has been revoked'}
        
        # except:
        
        #     return {'message': 'Something went wrong'}, 500

# class UserLogout(Resource):
#     """
#     User Logout Api 
#     """
#     @jwt_required
#     def get(self):

#         if 'username' in session:
#             session.pop('username', None)
#         return {'message' : 'You successfully logged out'}

class TokenRefresh(Resource):
    """
    Token Refresh Api
    """
    @jwt_required
    # @jwt_refresh_token_required
    def post(self):
        # Generating new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
    
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        
        return UserModel.return_all()

class UsersDeets(Resource):
        
    def get(self):
        
        data = parser.parse_args()
        username = data['username']
        # Searching user by username
        current_user = UserModel.find_by_username(username)
        
        # user does not exists
        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}
        
        # user exists, comparing password and hash
        if UserModel.verify_hash(data['password'], current_user.password):
            
            # generating access token and refresh token
            def to_json(x):
                return {

                    'username': x.username,
                    'name': x.name,
                    'email': x.email,
                    'password': x.password,
                    'profile_bio': x.profile_bio,
                    'rating': x.rating,
                    'flags': x.flags
                }
         
        return {'users': [to_json(current_user)]}
    
    def patch(self):
        parser.add_argument('username', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('profile_bio', required=True)
        # parser.add_argument('user_id', required=True)
        data = parser.parse_args()
        username = data['username']
        # name = data['name']
        # email = data['email']
        # profile_bio = data['profile_bio']
        # user_id = data['user_id']
        # Searching user by username
        current_user = UserModel.find_by_username(username)
        # user does not exists
        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}
    
        def to_json(x):
           
            x.username = data['username']
            x.email = data['email'] 
            x.name = data['name']
            x.profile_bio = data['profile_bio'] 
            db.session.commit()
            updated_user = x
            return {

                'name' :updated_user.name,
                'username':updated_user.username,
                'email': updated_user.email,
                'profile_bio':updated_user.profile_bio
            }
        
       
        return {'users': [to_json(current_user)]}


    def delete(self):

        data = parser.parse_args()
        username = data['username']
        # Searching user by username
        current_user = UserModel.find_by_username(username)

        db.session.delete(current_user)
        db.session.commit()
           
        if not current_user:
        
            return {'message': f'User {username} doesn\'t exist'}
        # return UserModel.delete_user(current_user) 
        return {'message': 'user deleted'}
        
class UsersFlags(Resource):
    def patch(self):
        parser.add_argument('flags', required=False)

        data = parser.parse_args()
        username = data['username']
        current_user = UserModel.find_by_username(username)
        # user does not exists
        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}
    
        def to_json(x):
           
            x.flags = data['flags']
            db.session.commit()
            updated_user = x

            if updated_user.flags == 4:
                RevokedTokenModel.add
            else:
                return {

                    'flags' :updated_user.flags,
                }
        
       

        return {'users': [to_json(current_user)]}

class UsersRating(Resource):
    def patch(self):
        parser.add_argument('rating', required=False)
        data = parser.parse_args()
        username = data['username']
        current_user = UserModel.find_by_username(username)
        # user does not exists
        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}
    
        def to_json(x):
            newrating = data['rating']
            print( 'new', newrating)
            x.rating = ( x.rating + int(newrating))/2
            db.session.commit()
            updated_user = x
            return {

                'rating' :updated_user.rating,

            }
        
      

        return {'users': [to_json(current_user)]}