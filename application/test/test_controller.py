import pytest
import application.controller
from flask import Flask
from application import app

#When we run this test we are going to need to update the data
def test_user_signup():
    data = {
        'username': 'Se',
        'password': 'Se',
        'name': 'Se',
        'email': 'Sey@outlook.com'
    }
    response = app.test_client().post('/signup', json=data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert additional conditions based on the expected behavior
    response_data = response.get_json()
    assert 'message' in response_data
    assert 'access_token' in response_data
    assert 'refresh_token' in response_data
    assert 'username' in response_data

    # Add more specific assertions if needed
    assert response_data['message'] == f'User {data["username"]} was created'
    assert response_data['username'] == data['username']

def test_user_signup_existing_user():
    data = {
        'username': 'sean',
        'password': 'sean',
        'name': 'Sean',
        'email': 'sean.obeirne@outlook.com'
    }
    response = app.test_client().post('/signup', json=data)

    # Assert that the response status code is 403 Forbidden
    assert response.status_code == 403

    # Assert additional conditions based on the expected behavior
    response_data = response.get_json()
    assert 'message' in response_data
    assert response_data['message'] == f'User {data["username"]} already exists'

def test_user_login():
    data = {
        'username': 'sean',
        'password': 'sean'
    }
    response = app.test_client().post('/login', json=data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert additional conditions based on the expected behavior
    response_data = response.get_json()
    assert 'message' in response_data
    assert 'access_token' in response_data
    assert 'refresh_token' in response_data
    assert 'username' in response_data

    # Add more specific assertions if needed
    assert response_data['message'] == f'Logged in as {data["username"]}'
    assert response_data['username'] == data['username']

def test_user_login_nonexistent_user():
    data = {
        'username': 'nonexistent',
        'password': 'password'
    }
    response = app.test_client().post('/login', json=data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert additional conditions based on the expected behavior
    response_data = response.get_json()
    assert 'message' in response_data
    assert response_data['message'] == f'User {data["username"]} doesn\'t exist'

def test_user_login_wrong_credentials():
    data = {
        'username': 'sean',
        'password': 'wrong_password'
    }
    response = app.test_client().post('/login', json=data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert additional conditions based on the expected behavior
    response_data = response.get_json()
    assert 'message' in response_data
    assert response_data['message'] == 'Wrong credentials'

# def test_user_logout_access():
#     # Assuming the user is already authenticated and has a valid access token  
#     with app.test_client() as client:
#         access_token = "<actual_access_token>"  # Replace with the actual access token
#         # Send a POST request to logout from access token
#         response = client.post('/logout/access', headers={'Authorization': f'Bearer {access_token}'})
        
#         # Assert that the response status code is 200 OK
#         assert response.status_code == 200

#         # Assert additional conditions based on the expected behavior
#         response_data = response.get_json()
#         assert 'message' in response_data
#         assert response_data['message'] == 'Access token has been revoked'

# def test_token_refresh():
#     # Assuming the user is already authenticated and has a valid refresh token
#     with app.test_client() as client:
#         # Send a POST request to refresh the access token
#         response = client.post('/token/refresh', headers={'Authorization': 'Bearer <refresh_token>'})

#         # Assert that the response status code is 200 OK
#         assert response.status_code == 200

#         # Assert additional conditions based on the expected behavior
#         response_data = response.get_json()
#         assert 'access_token' in response_data

#         # Add more specific assertions if needed
#         assert response_data['access_token'] != '<refresh_token>'

# def test_users_flags():
#     # Assuming the user is already authenticated and has a valid access token
#     with app.test_client() as client:
#         # Send a PATCH request to update user flags
#         data = {'username': 'sean', 'flags': 4}
#         headers = {'Authorization': 'Bearer <access_token>'}
#         response = client.patch('/users/flags', json=data, headers=headers)
        
#         # Assert that the response status code is 200 OK
#         assert response.status_code == 200
        
#         # Assert the response data based on the expected behavior
#         response_data = response.get_json()
#         assert 'users' in response_data
#         assert 'flags' in response_data['users'][0]
#         assert response_data['users'][0]['flags'] == 4

# def test_user_login_two():
#     data = {'username': 'sean', 'password': 'sean', 'name': 'Sean', 'email': 'sean.obeirne@outlook.com'}
#     response = app.test_client().post('/login', json=data)

#     # Assert that the response status code is 200 OK
#     assert response.status_code == 200

#     # Extract the access token from the response
#     response_data = response.get_json()
#     access_token = response_data['access_token']

#     # Use the access token in subsequent requests
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = app.test_client().get('/protected', headers=headers)

#     # Assert the response based on the expected behavior
#     assert response.status_code == 200
#     assert 'message' in response.get_json()
