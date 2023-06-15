from application import app, db
from application.models.users_models import UserModel, Language, Game

app.app_context().push()
db.drop_all()
db.create_all()
print("Database tables created")

user1 = UserModel(username='Bob', password='builder', name='Bob', email='bob@builder.com')

user2 = UserModel(username='Wendy', password='builder', name='Wendy', email='wendy@builder.com')

language1 = Language(language_name='French', flag_base64="PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj4NCjxwYXRoIGZpbGw9IiNlZDI5MzkiIGQ9Im0wLDBoOTAwdjYwMGgtOTAweiIvPg0KPHBhdGggZmlsbD0iI2ZmZiIgZD0ibTAsMGg2MDB2NjAwaC02MDB6Ii8+DQo8cGF0aCBmaWxsPSIjMDAyMzk1IiBkPSJtMCwwaDMwMHY2MDBoLTMwMHoiLz4NCjwvc3ZnPg0K")
language2 = Language(language_name='Italian', flag_base64='')
language3 = Language(language_name='Dutch', flag_base64='')
language4 = Language(language_name='German', flag_base64="PHN2ZyB3aWR0aD0iMTAwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBoZWlnaHQ9IjYwMCIgdmlld0JveD0iMCAwIDUgMyI+DQo8cGF0aCBkPSJtMCwwaDV2M2gtNXoiLz4NCjxwYXRoIGZpbGw9IiNkMDAiIGQ9Im0wLDFoNXYyaC01eiIvPg0KPHBhdGggZmlsbD0iI2ZmY2UwMCIgZD0ibTAsMmg1djFoLTV6Ii8+DQo8L3N2Zz4NCg==")
language5 = Language(language_name= 'English', flag_base64="PHN2ZyB3aWR0aD0iMTIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2aWV3Qm94PSIwIDAgNjAgMzAiIGhlaWdodD0iNjAwIj4NCjxkZWZzPg0KPGNsaXBQYXRoIGlkPSJ0Ij4NCjxwYXRoIGQ9Im0zMCwxNWgzMHYxNXp2MTVoLTMwemgtMzB2LTE1enYtMTVoMzB6Ii8+DQo8L2NsaXBQYXRoPg0KPC9kZWZzPg0KPHBhdGggZmlsbD0iIzAwMjQ3ZCIgZD0ibTAsMHYzMGg2MHYtMzB6Ii8+DQo8cGF0aCBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iNiIgZD0ibTAsMGw2MCwzMG0wLTMwbC02MCwzMCIvPg0KPHBhdGggc3Ryb2tlPSIjY2YxNDJiIiBzdHJva2Utd2lkdGg9IjQiIGQ9Im0wLDBsNjAsMzBtMC0zMGwtNjAsMzAiIGNsaXAtcGF0aD0idXJsKCN0KSIvPg0KPHBhdGggc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEwIiBkPSJtMzAsMHYzMG0tMzAtMTVoNjAiLz4NCjxwYXRoIHN0cm9rZT0iI2NmMTQyYiIgc3Ryb2tlLXdpZHRoPSI2IiBkPSJtMzAsMHYzMG0tMzAtMTVoNjAiLz4NCjwvc3ZnPg0K")

game1 = Game(game_name='GTA5', platform="PlayStation")
game2 = Game(game_name='CoD', platform = "PlayStation")
game3 = Game(game_name='Total War', platform = "PC")
game4 = Game(game_name='FIFA')
game5 = Game(game_name='Squad', platform = "PC")

user1.languages_known.append(language1)
user1.languages_learn.append(language3)
user2.languages_known.append(language3)
user2.languages_learn.append(language1)

user1.games.append(game1)
user1.games.append(game5)
user2.games.append(game2)
user2.games.append(game4)

user1.connections.append(user2)
user2.connections.append(user1)


db.session.add_all([user1,user2])
db.session.add_all([language1,language2,language3,language4,language5,])
db.session.add_all([game1,game2,game3,game4,game5,])

db.session.commit()
print("Database seeded")

print (user1.games)
