'''
Now we're using the User `@classmethod`s
for username mapping instead of the 
set comprehensions.
'''

from werkzeug.security import safe_str_cmp
from user import User


##
#  Removed list and mapping variables
#  - We're storing users in a database
#  - We're retrieving users from the database
##

def authenticate(username, password):
    # Use the User class methods
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
