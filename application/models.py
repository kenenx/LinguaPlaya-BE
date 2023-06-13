

from application import app,db

from passlib.hash import pbkdf2_sha256 as sha256

app.app_context().push()
db.create_all()

class UserModel(db.Model):
    """
    User Model Class
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(120), nullable=False)

    """
    Save user details in Database
    """
    def save_to_db(self):

        db.session.add(self)

        db.session.commit()

    """
    Find user by username
    """
    @classmethod
    def find_by_username(cls, username):
        
        return cls.query.filter_by(username=username).first()

    """
    return all the user data in json form available in DB
    """
    @classmethod
    def return_all(cls):
        
        def to_json(x):
        
            return {
        
                'username': x.username,
        
                'password': x.password
        
            }
        
        return {'users': [to_json(user) for user in UserModel.query.all()]}

    """
    Delete user data
    """
    @classmethod
    def delete_all(cls):
        
        try:
        
            num_rows_deleted = db.session.query(cls).delete()
        
            db.session.commit()
        
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        
        except:
        
            return {'message': 'Something went wrong'}

    """
    generate hash from password by encryption using sha256
    """
    @staticmethod
    def generate_hash(password):
        
        return sha256.hash(password)

    """
    Verify hash and password
    """
    @staticmethod
    def verify_hash(password, hash_):
        
        return sha256.verify(password, hash_)


class RevokedTokenModel(db.Model):
    """
    Revoked Token Model Class
    """

    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    
    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """
    def add(self):
    
        db.session.add(self)
    
        db.session.commit()

    """
    Checking that token is blacklisted
    """
    @classmethod
    def is_jti_blacklisted(cls, jti):
    
        query = cls.query.filter_by(jti=jti).first()
    
        return bool(query)


##############################################################
import datetime
from application import app,db

app.app_context().push()
db.create_all()

# user models 
# class Users(db.Model):
#     users_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     username =  db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     registered_on = db.Column(db.DateTime, nullable=False)
#     # rating = db.Column(db.Integer, nullable=False, default = 5)
#     # flags = db.Column(db.Integer, nullable=False, default = 0)
#     # not sure about these
#     # connections = db.Column(db.Integer, foreign_key = True)
#     # time_zone = db.Column(db.Integer, nullable=False)
#     # last_online = db.Column(db.Integer, nullable=False)

# #rating,flags, connections, time_zone, last_online
#     def __init__(self, name, email, username, password ):
#         self.name = name
#         self.email = email
#         self.username = username
#         self.password = bcrypt.generate_password_hash(
#             password, app.config.get('BCRYPT_LOG_ROUNDS')
#         ).decode()
#         # self.rating = rating
#         # self.flags = flags
#         # self.connections = connections
#         # self.time_zone = time_zone
#         # self.last_online = last_online
#         self.registered_on = datetime.datetime.now()
    


with app.app_context():
    db.create_all()
    print("Database tables created")
