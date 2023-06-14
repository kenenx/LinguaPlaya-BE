# from flask_restful import Resource, reqparse
# from flask import session
# from application.models.users_models import UserModel, RevokedTokenModel
# import json

# parser = reqparse.RequestParser()

# parser.add_argument('username', required=True)

# class UserGet(Resource):
#     #/user/<user_id>
#     def get(self):
#         data = parser.parse_args()
#         user = data['username']
#         currentuser = UserModel.find_by_username(user)
#         print (currentuser)
#         return json.dumps(currentuser)
    
#     def delete(self):
#         data = parser.parse_args()
#         user_id = data['username']
#         return UserModel.find_by_id(user_id)
