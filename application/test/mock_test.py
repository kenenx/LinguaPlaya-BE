import pytest
import application.auth_mid
from flask import Flask
app = Flask(__name__)
users = []
@pytest.fixture
def api(monkeypatch):
    test_users = [{'user_id': 1, 'username': 'testingUserName','name': 'testingName','email': 'testing@Name.com', 'password':'regefgfg'}, { 'username': 'NameTest', 'password':'wesdddsgd'}]
    monkeypatch.setattr(application.auth_mid, "users", test_users)
    api = application.auth_mid.app.test_client()
    return api
