import json
import application.controller
import application.routes
import unittest
from application import app,db
from application.models.users_models import UserModel

class modeltests(unittest.TestCase):
    
    def test_savetodb(self):
        self.app = app.test_client()
        payload = json.dumps({
                    'username': 'creatingTestUser',
                    'name': 'Molly',
                    'email':'created@me.com',
                    'password':'elloagain'
                })
      
        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)
        response.save_to_db(self)
        self.assertEqual(str, type(response.json['message']))
