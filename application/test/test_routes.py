import pytest
import application.routes
from flask import Flask
from application import app

def test_hello_world():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Welcome to the backend fool! MORE INFO TO COME'}

def test_user_signup():
    # When we run final coverage report we will see that this test is not being run, we will just have to put in new data and it will pass
    data = {'username': 'B', 'password': 'B', 'name': 'J', 'email': 'Bjack@hotmail.com'}
    response = app.test_client().post('/signup', json=data)
    assert response.status_code == 200

def test_user_login():
    data = {
        'username': 'sean',
        'password': 'sean',
        'name': 'Sean',
        'email': 'sean.obeirne@outlook.com'
    }
    response = app.test_client().post('/login', json=data)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert additional conditions based on the expected behavior
    # For example, you can check if the response contains a specific message or data
    response_data = response.get_json()
    assert 'message' in response_data
    assert 'access_token' in response_data
