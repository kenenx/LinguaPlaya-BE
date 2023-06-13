import pytest
import users_routes

@pytest.fixture
def api(monkeypatch):
    test_users = [{'users_id': 1, 'name': 'testingName', 'password':'regefgfg'}, {'id': 2, 'name': 'NameTest', 'password':'wesdddsgd'}]
    monkeypatch.setattr(users_routes, "users", test_users)
    app = users_routes.app.test_client()
    return app
