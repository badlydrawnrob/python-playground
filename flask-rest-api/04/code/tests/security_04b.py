from werkzeug.security import safe_str_cmp
from user_04 import User

# We need to create a store of
# users, and also have the ability
# to quickly look them up by username,
# or id.
#
# - This means we don't have to loop
#   through users everytime we want to
#   find their details!

users = [
    # These user objects are essentially,
    # the same as {id: 1, 'username': ...}
    User(1, 'bob', 'asdf'),
    User(2, 'alice', 'cdfg')
]

# This will give a list of keys and user objects
# .. 'bob': <__main__.User object at 0x10d290358>
username_mapping = {u.username: u for u in users}

# e.g:
# username_mapping['bob']

userid_mapping = {u.id: u for u in users}

# e.g:
# userid_mapping[1]


# We now need to generate a JSON web token (JWT)
# so that we can verify their details, send them a token
# and they can send this token along with any
# requests made.

def authenticate(username, password):
    # .get() allows us to access a dictionary with it's key
    # ... We can also add a default, 'None'
    #
    # .get('bob', None) returns <__main__.User object at 0x10d290358>
    # - You can then access user.id, user.username etc
    user = username_mapping.get(username, None)
    # It's best not to compare strings with `==`,
    # as utf8 / unicode characters can give wrong results
    # - However, we can user `safe_str_cmp` for now:
    if user and safe_str_cmp(user.password, password):
        return user

# This function is unique to `flask_JWT`
# - the payload is the contents of the JWT token
def identity(payload):
    # Retrieve the user with the current token
    # - dictionary with user.id
    user_id = payload['identity']
    # Now we have the user.id, we can
    # extract it with our userid mapping
    # .get(1, None)
    return userid_mapping.get(user_id, None)

