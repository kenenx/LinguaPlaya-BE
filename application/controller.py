from flask_restful import Resource, reqparse
from flask import session, request
import json
from application import app,db
from application.models.users_models import UserModel, RevokedTokenModel, Language, Game, user_game

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

import pdb


parser = reqparse.RequestParser()

parser.add_argument('username', help='username cannot be blank', required=False)
parser.add_argument('password', help='password cannot be blank', required=False)

class UserSignup(Resource):
    """
    User Registration Api
    """
   
    def post(self):
        parser.add_argument('email', help='email cannot be blank', required=False)
        parser.add_argument('name', help='name cannot be blank', required=False)
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

#class UsersDeets(Resource):
        
    # def get(self,username):
    #     parser.add_argument('username', help='username cannot be blank', required=False)
        
    #     data = parser.parse_args()
    #     #username = data['username']
    #     # Searching user by username
    #     current_user = UserModel.find_by_username(username)
        
    #     # user does not exists
    #     # if not current_user:
    #     #     return {'message': f'User {username} doesn\'t exist'}
        
    #     # user exists, comparing password and hash
    #     #if UserModel.verify_hash(data['password'], current_user.password):
            
    #         # generating access token and refresh token
    #     def to_json(x):
    #         return {

    #             'username': x.username,
    #             'name': x.name,
    #             'email': x.email,
    #             'password': x.password,
    #             'profile_bio': x.profile_bio,
    #             'rating': x.rating,
    #             'flags': x.flags,
    #         #     'languages_known': x.languages_known,
    #         #     'languages_learn': x.languages_learn,
    #         #     'games': x.games,
    #         #     'connections': x.connections
    #         }
        
    #     return {'users': [to_json(current_user)]}
    
    # def patch(self):
    #     parser.add_argument('username', required=False)
    #     parser.add_argument('email', required=False)
    #     parser.add_argument('name', required=False)
    #     parser.add_argument('profile_bio', required=False)
    #     # parser.add_argument('games', required=False)
    #     # parser.add_argument('languages_known', required=False)
    #     # parser.add_argument('languages_learn', required=False)
    #     # parser.add_argument('', required=False)
    #     # parser.add_argument('user_id', required=True)
    #     data = parser.parse_args()
    #     username = data['username']
    #     # name = data['name']
    #     # email = data['email']
    #     # profile_bio = data['profile_bio']
    #     # user_id = data['user_id']
    #     # Searching user by username
    #     current_user = UserModel.find_by_username(username)
    #     # user does not exists
    #     if not current_user:
    #         return {'message': f'User {username} doesn\'t exist'}
    
    #     def to_json(x):
           
    #         x.username = data['username']
    #         x.email = data['email'] 
    #         x.name = data['name']
    #         x.profile_bio = data['profile_bio'] 
    #         db.session.commit()
    #         updated_user = x
    #         return {

    #             'name' :updated_user.name,
    #             'username':updated_user.username,
    #             'email': updated_user.email,
    #             'profile_bio':updated_user.profile_bio,
    #             'games':updated_user.games,
    #             'languages_known' : updated_user.languages_known,
    #             'languages_learn': updated_user.languages_learn,
    #             'connections': updated_user.connections

    #         }
        
       
    #     return {'users': [to_json(current_user)]}


    # def delete(self):

    #     data = parser.parse_args()
    #     username = data['username']
    #     # Searching user by username
    #     current_user = UserModel.find_by_username(username)

    #     db.session.delete(current_user)
    #     db.session.commit()
           
    #     if not current_user:
        
    #         return {'message': f'User {username} doesn\'t exist'}
    #     # return UserModel.delete_user(current_user) 
    #     return {'message': 'user deleted'}
        
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
    
class AllLanguages(Resource):
    def get(self):
        return Language.return_all()
    
class Languages(Resource):
    def post(self):
        parser.add_argument('language_name', help='language cannot be blank', required=False)
        data = parser.parse_args()

        language_name = data['language_name']
        # flag_base64 = data['flag_base64']

        # Checking that user is already exist or not
        if Language.find_by_name(language_name):
            return {'message': f'{language_name} already exists'}
        # create new language
        new_language = Language(
            language_name=language_name,
            # flag_base64= flag_base64,
        )
        try:
            new_language.save_to_db()
            return {
                'message': f'{language_name} was created',
            }
        except (RuntimeError, TypeError, NameError, ValueError):
            return RuntimeError, TypeError, NameError, ValueError
        
# class UserGames(Resource):

#     def get(self):
#         parser.add_argument('user_id', help='game cannot be blank', required=False)
#         data = parser.parse_args()
#         user_id = data['user_id']
#         current_user = UserModel.find_by_id(user_id)
#         def to_json(x):
#             return {
#                 'username': x.username,
#                 'games': x.games
#             }

#         return UserModel.find_user_games(user_id)

class UserGames(Resource):

    def get(self):
        
        parser.add_argument('user_id', help='game cannot be blank', required=False)
        parser.add_argument('username', help='username cannot be blank', required=False)
        data = parser.parse_args()
        user_id = data['user_id']
        username = data['username']
        current_user = UserModel.find_by_username(username)
        # listgames = str(listgames)
        # usergames = db.session.query.join(user_game.user_game_id).filter(user_game.user_id == self.user_id).all()
        # listgames = self.query.join(Game.game_id).join(UserModel.games).filter(user_id == UserModel.user_id).all()
        def to_json(x):
            return {
                'username': x.username,
                'games': x.games
            }
        print (current_user)
        # plzwork = db.session.query(UserModel, user_game).filter(UserModel.user_id == user_game.user_id,).filter( UserModel.user_id == user_id,).all()
        plzwork = UserModel.find_user_games(user_id)

        return {'users': [to_json(plzwork)]}
    
    # plzwork = db.session.query(UserModel, Game).filter(UserModel.user_id == Game.user_id,).filter( UserModel.username == current_user,).all()

class AllGames(Resource):
    def get(self):
        return Game.return_all()
    
class Games(Resource):
    def post(self):
        parser.add_argument('game_name', help='game cannot be blank', required=False)
        parser.add_argument('platform', help='platform cannot be blank', required=False)
        data = parser.parse_args()

        game_name = data['game_name']
        platform = data['platform']

        # Checking that user is already exist or not
        if Game.find_by_name(game_name):
            return {'message': f'{game_name} already exists'}
        # create new language
        new_game = Game(
            game_name=game_name,
            platform=platform,
        )
        try:
            new_game.save_to_db()
            return {
                'message': f'{game_name} was created',
            }
        except (RuntimeError, TypeError, NameError, ValueError):
            return RuntimeError, TypeError, NameError, ValueError
