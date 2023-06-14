# To do list for backend
## left to do
- Users
    - logout feature
    - connection to:
        - user_lang
        - user_games
        - friends(connections)
        - posts
- Lang
    - table of lang and flags
    - user_lang table
        - known
        - learning
- Games
    - users games (steam API)
- connections
    - friends made/list of connections between users
    - message log?
- posts
    - users posts

### Users

|GET| /<id> | Get the user that logged in |
|PATCH| /<id>| Update user details |
|DELETE| /<id> | Delete account |

### Auth/Token gen
|POST| /login | user logging in and getting them there access token|
|POST| /signup| adding the user signing up data to the db and creating thme an access token|
|POST| /logout | logging the user out and deleting there access token |
### Languges - user_lang
|GET| /languges| for commminuty page filters |
|GET| /user_lang/known | to display users know langs |
|GET| /user_lang/learning | to display users langs they want to learn|
|POST| /user_lang| |
|POST| /logout | logging the user out and deleting there access token |
### Games - user_games
### friends (connections)
### posts
