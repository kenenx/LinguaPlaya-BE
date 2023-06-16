import datetime
from flask import jsonify
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


from application import app,db
from passlib.hash import pbkdf2_sha256 as sha256

# app.app_context().push()
# db.drop_all()
# db.create_all()

user_language_known = db.Table('user_language_known',
                          db.Column('user_language_known_id',db.Integer, primary_key=True),
                          db.Column('user_id',db.Integer, db.ForeignKey('users.user_id')),
                          db.Column('language_id',db.Integer, db.ForeignKey('language.language_id'))
                          )

user_language_learn = db.Table('user_language_learn',
                          db.Column('user_language_learn_id',db.Integer, primary_key=True),
                          db.Column('user_id',db.Integer, db.ForeignKey('users.user_id')),
                          db.Column('language_id',db.Integer, db.ForeignKey('language.language_id'))
                          )

user_game = db.Table('user_game',
                     db.Column('user_game_id',db.Integer, primary_key=True),
                     db.Column('user_id',db.Integer, db.ForeignKey('users.user_id')),
                     db.Column('game_id',db.Integer, db.ForeignKey('game.game_id')))

user_connection = db.Table('user_connection',
                        db.Column('connection_id',db.Integer, primary_key=True),
                        db.Column('user_Parent_id',db.Integer, db.ForeignKey('users.user_id')),
                        db.Column('user_Child_id',db.Integer, db.ForeignKey('users.user_id')))

class UserModel(db.Model):
    """
    User Model Class
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ###################################################
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    # registered_on = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default = 5)
    flags = db.Column(db.Integer, nullable=False, default = 0)
# not sure about these yet
#     # connections_id = db.Column(db.Integer, foreign_key = True)
#     # langauges_id = db.Column(db.Integer, foreign_key = True)
#     # games_id = db.Column(db.Integer, foreign_key = True)
    profile_bio = db.Column(db.String(500), nullable=True)
    time_zone = db.Column(db.Integer, nullable=True)
    last_online = db.Column(db.Integer, nullable=True)
    # user_languages = db.relationship('UserLanguage', backref='users')
    languages_known = db.relationship('Language', secondary=user_language_known, backref='known', cascade="all,delete")
    languages_learn = db.relationship('Language', secondary=user_language_learn, backref='learn', cascade="all,delete")
    games = db.relationship('Game', secondary=user_game, backref='users', cascade="all,delete")
    connections = db.relationship('UserModel', secondary=user_connection, primaryjoin=user_id==user_connection.c.user_Parent_id,
                                  secondaryjoin=user_id==user_connection.c.user_Child_id,backref=('parent')
                                  )

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

    @classmethod
    def find_by_id(cls, user_id):
            
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_user_games(cls, user_id):
        # query.join(user_game).join(Game).filter(user_game.c.user_id == cls.user_id) & (user_game.c.game_id == Game.game_id).all()

        # return db.session.query.join(user_game).join(Game).filter(user_game.c.user_id == cls.user_id) & (user_game.c.game_id == Game.game_id).all()
        return cls.query(cls).join(user_game, cls.user_id == user_game.user_id).filter(cls.user_id== user_id).all()
        
    """
    return all the user data in json form available in DB
    """
    @classmethod
    def return_all(cls):
        
        def to_json(x):
        
            return {
        
                'username': x.username,
                'name': x.name,
                'email': x.email,
                'rating': x.rating,
                # "flags": x.flags,
                "profile_bio": x.profile_bio,
                # "time_zone" : x.time_zone,
                # "last_online": x.last_online
        
            }
        
        return {'users': [to_json(user) for user in UserModel.query.all()]}

    # """
    # Delete user data
    # """
    # @classmethod
    # def delete_user(cls, username):
        
    #     try:
           
    #         num_rows_deleted = cls.query.filter_by(username=username).first()
    #         print('hello')
    #         obj = cls.query.filter_by(num_rows_deleted).one()
    #         db.session.delete(obj)
    #         db.session.commit()
           
    #         return {'message': f'{username} is deleted'}
        
    #     except:
        
    #         return {'message': 'Something went wrong'}

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

# user models 
# class Users(db.Model):

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

# class UserLanguage(db.Model):
#     user_languages_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
#     language_id = db.Column(db.Integer, ForeignKey("language.language_id"))
#     level = db.Column(db.String(1000), nullable = True)

# user_language = db.Table('user_language',
#                           db.Column('user_id',db.Integer, db.ForeignKey('users.user_id')),
#                           db.Column('language_id',db.Integer, db.ForeignKey('language.language_id'))
#                           )
    
class Language(db.Model):

    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(100),unique=True, nullable=False)
    flag_base64 = db.Column(db.String(2000), nullable=True)
    """
    Save language details in Database
    """
    def save_to_db(self):

        db.session.add(self)
        db.session.commit()
    """
    Find language by name
    """
    @classmethod
    def find_by_name(cls, language_name):
        return cls.query.filter_by(language_name=language_name).first()
    
    @classmethod
    def find_by_id(cls, language_id):
        return cls.query.filter_by(language_id=language_id).first()
    """
    return all the languages
    """
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'language_id': x.language_id,
                'language_name': x.language_name,
                # 'flag_base64': x.email,
            }
        return {'languages': [to_json(language) for language in Language.query.all()]}

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=True)
    """
    Save game details in Database
    """
    def save_to_db(self):

        db.session.add(self)
        db.session.commit()
    """
    Find game by name
    """
    @classmethod
    def find_by_name(cls, game_name):
        return cls.query.filter_by(game_name=game_name).first()
    
    @classmethod
    def find_by_id(cls, game_id):
        return cls.query.filter_by(game_id=game_id).first()
    """
    return all the games
    """
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'game_id': x.game_id,
                'game_name': x.game_name,
                'platform': x.platform,
            }
        return {'games': [to_json(game) for game in Game.query.all()]}
    
@app.route("/users/connections")
def get_users_connections():
    user_query = db.session.query(UserModel, Game, user_game).join(UserModel).join(Game).all()
    result = []
    for row in user_query:
        result.append({
            'Parent_id': row.user_id,
            'Child_id': row.user_id
        })
    return jsonify(result)

@app.route("/users/languages")
def get_users_languages():
    user_query = db.session.query(UserModel, user_language_known, user_language_learn).all()
        # join(user_language_known, UserModel.user_id == user_language_known.user_id).\
        #     join(user_language_learn, UserModel.user_id == user_language_learn.user_id).\
        #         join(Language, Language.id == user_language_known.language_id).\
        #             join(Language, Language.id == user_language_learn.language_id).all()
    result = []
    print(user_query)
    for row in user_query:
        result.append({
            # 'user_id': row.user_id,
            # 'language_id_known': row.language_id,
            'username': row.UserModel.username,
            'language_learn': row[4],
            'language_known': row[5]
        })
    return jsonify(result)

@app.route("/users/languages_known")
def get_users_languages_known():
    user_query = db.session.query(UserModel, user_language_known, Language).join(UserModel).join(Language).all()
    result = []
    print(user_query)
    for row in user_query:
        result.append({
            'user_id': row.user_id,
            'language_id_known': row.language_id,
            'username': row.UserModel.username,
            'language_learn': row.Language.language_name
        })
    return jsonify(result)

@app.route("/users/languages_learn")
def get_users_languages_learn():
    user_query = db.session.query(UserModel, user_language_learn, Language).join(UserModel).join(Language).all()
    result = []
    print(user_query)
    for row in user_query:
        result.append({
            # 'user_id': row.user_id,
            # 'language_id_learn': row.language_id,
            'username': row.UserModel.username,
            'language_known': row.Language.language_name
        })
    return jsonify(result)

@app.route("/users/games")
def get_users_games():
    user_query = db.session.query(UserModel, Game, user_game).join(UserModel).join(Game).all()
    print(user_query)
    result = []
    for row in user_query:
        result.append({
            # 'user_id': row.user_id,
            # 'game_id': row.game_id,
            'username': row.UserModel.username,
            'game_name': row.Game.game_name
        })
    return jsonify(result)

@app.route("/users/getall")
def get_users_all():
    user_query = db.session.query(UserModel, Game, user_game).join(UserModel).join(Game).all()
    print(user_query)
    result = []
    for row in user_query:
        result.append({
            'user_id': row.user_id,
            'game_id': row.game_id,
            'username': row.UserModel.username,
            'game_name': row.Game.game_name
        })
    return jsonify(result)