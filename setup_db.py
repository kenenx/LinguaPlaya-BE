from application import app, db
from application.models.users_models import UserModel, Language

app.app_context().push()
db.drop_all()
db.create_all()
print("Database tables created")

user1 = UserModel(username='Bob', password='builder', name='Bob', email='bob@builder.com')

user2 = UserModel(username='Wendy', password='builder', name='Wendy', email='wendy@builder.com')

language1 = Language(language_name='French')
language2 = Language(language_name='Italian')
language3 = Language(language_name='Spanish')
language4 = Language(language_name='German')
language5 = Language(language_name= 'English')

user1.languages.append(language1)
user1.languages.append(language3)

user2.languages.append(language4)
user2.languages.append(language5)

db.session.add_all([user1,user2])
db.session.add_all([language1,language2,language3,language4,language5,])

db.session.commit()
print("Database seeded")
