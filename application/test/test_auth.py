
import json
import unittest
from application.models.users_models import UserModel
from flask_testing import TestCase
import application.controller
import application.routes
from application import app, db



class test_user_login_signup(unittest.TestCase):
    # def test_signup_auth(self):
    #     return self.client.post(
    #         '/signup',
    #         data = json.dumps({
    #                 'username': 'creatingTestUser',
    #                 'name': 'Molly',
    #                 'email':'created@me.com',
    #                 'password':'elloagain'
    #                 }),
    #     content_type='application/json',
    #     )

    # def login_user(self, email,name, username, password):
    #     return self.client.post(
    #         '/login',
    #         data=json.dumps(dict(
    #             email=email,
    #             password=password,
    #             name=name,
    #             username = username
    #         )),
    #         content_type='application/json',
    #     )
    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        self.app = app.test_client()
        payload = json.dumps({
                'username': 'creatingTestUser10',
                'name': 'Molly',
                'email':'created@me.com',
                'password':'elloagain'
            })
        # db.session.add(payload)
        # db.session.commit()
        # with self.client:
        #     response = test_signup_auth(self,'created@me.com','Molly', 'creatingTestUser5', 'elloagain')
        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        data = json.loads(response.data.decode())
        
        # self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

# class test_signup_auth(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()
    
#         response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

#         self.assertEqual(str, type(response.json['access_token']))
#         self.assertEqual(200, response.status_code)
