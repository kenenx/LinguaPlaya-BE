import json
import users_routes

def test_api_get_user(app):
    res = app.get('/app/users/2')
    assert res.json['users']['name'] == 'NameTest'

def test_api_post_users(app):
    mock_data = json.dumps({'name': 'creatingTestUser'})
    mock_headers = {'Content-Type': 'application/json'}
    res = app.post('/api/users', data=mock_data, headers=mock_headers)
    assert res.json['users']['id'] == 3

def test_api_not_found(app):
    res = app.get('/notArealAPI')
    assert res.status == '404 NOT FOUND'
    assert 'Oops!' in res.json['message']
    