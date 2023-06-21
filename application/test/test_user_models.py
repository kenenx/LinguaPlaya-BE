import pytest
import application.models.users_models
from flask import Flask
from application import app, db
from application.models.users_models import UserModel, RevokedTokenModel

# Test UserModel
def test_user_model():
    # Create a test user
    user = UserModel(username='john', name='John Doe', email='john@example.com', rating=4.5)

    # Verify the user attributes
    assert user.username == 'john'
    assert user.name == 'John Doe'
    assert user.email == 'john@example.com'
    assert user.rating == 4.5

    # Test generate_hash method
    password = 'password123'
    hashed_password = UserModel.generate_hash(password)
    assert UserModel.verify_hash(password, hashed_password)  # Verify the generated hash

# Initialize the test database
@pytest.fixture(scope='module')
def test_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

# Test RevokedTokenModel
def test_revoked_token_model(test_database):
    # Create a test revoked token
    token = RevokedTokenModel(jti='123456')

    # Verify the token attribute
    assert token.jti == '123456'

    # Test add method
    token.add()  # Add the token to the database

    # Test is_jti_blacklisted method
    assert RevokedTokenModel.is_jti_blacklisted('123456')  # Verify that the token is blacklisted

# Run the tests
if __name__ == '__main__':
    pytest.main()
