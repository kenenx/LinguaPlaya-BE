import json
import application.controller
import application.routes
import unittest
from application import app,db

def test_backend_exsits(app):
    res = app.get('/')
    assert res.json['message']

class test_signup(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    def test_api_post_users_signup(self):
        payload = json.dumps({
                'username': 'creatingTestUser',
                'name': 'Molly',
                'email':'created@me.com',
                'password':'elloagain'
            })

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(str, type(response.json['message']))
        self.assertEqual(200, response.status_code)

        