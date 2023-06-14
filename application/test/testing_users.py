import json
import application.auth_mid

def test_backend_exsits(app):
    res = app.get('/')
    assert res.json == {'Welcome to the backend fool! MORE INFO TO COME'}
# def test_api_get_user(app):
#     res = app.get('/')
#     assert res.json['users']['username'] == 'NameTest'

def test_api_post_users_login(app):
    mock_data = json.dumps({'username': 'creatingTestUser', 'name': 'Molly', 'email':'created@me.com', 'password':'elloagain' })
    mock_headers = {'Content-Type': 'application/json'}
    res = app.post('/login', data=mock_data, headers=mock_headers)
    assert res.json['users']['id'] == 3
