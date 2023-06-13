import pytest
import __init__

@pytest.fixture
def api(monkeypatch):
    test_users = [{'users_id': 1, 'name': 'testingName', 'password':'regefgfg'}, {'id': 2, 'name': 'NameTest', 'password':'wesdddsgd'}]
    monkeypatch.setattr(__init__, "users", test_users)
    app = __init__.app.test_client()
    return app
