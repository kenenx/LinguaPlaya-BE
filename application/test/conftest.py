import pytest
import application.routes
import application.controller
import application.models.users_models
# import pytest
import application.controller
import application.routes
from flask import Flask

app = Flask(__name__)
#app = app()
app.config.update({
        "TESTING": True,
})
# users = []
@pytest.fixture
def app(monkeypatch):
    
    test_users = [{'user_id': 1, 'username': 'testingUserName','name': 'testingName','email': 'testing@Name.com', 'password':'regefgfg'}, { 'username': 'NameTest', 'password':'wesdddsgd'}]
    # monkeypatch.setattr(application.models.users_models, "UserModel", test_users)
    monkeypatch.setattr(application.routes, "controller", test_users)
    monkeypatch.setattr(application.controller, "UserSignup", test_users)
    app = application.routes.app.test_client()
    return app



# @pytest.fixture()


#     # other setup can go here

#     yield app

#     # clean up / reset resources here


# @pytest.fixture()
# def client(app):
#     return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()
