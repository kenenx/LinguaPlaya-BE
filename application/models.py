
import jwt
import datetime
from application import app,db, bcrypt

app.app_context().push()
db.create_all()

# user models 
class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username =  db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
    registered_on = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    flags = db.Column(db.Integer, nullable=False)
    # not sure about these
    connections = db.Column(db.Integer, foreign_key = True)
    time_zone = db.Column(db.Integer, nullable=False)
    last_online = db.Column(db.Integer, nullable=False)


    def __init__(self, name, age, email, username, password, rating,flags, connections, time_zone, last_online):
        self.name = name
        self.age = age
        self.email = email
        self.username = username
        self.password = password
        self.rating = rating
        self.flags = flags
        self.connections = connections
        self.time_zone = time_zone
        self.last_online = last_online
        self.registered_on = datetime.datetime.now()
    
    # Generates the Auth Token
    def encode_auth_token(self, users_id):
       
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': users_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    #Validates the auth token    
    @staticmethod
    def decode_auth_token(auth_token):
       
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
with app.app_context():
    db.create_all()
    print("Database tables created")

# Token Model for storing JWT tokens
class BlacklistToken(db.Model):

    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
    
    # check whether auth token has been blacklisted
    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


