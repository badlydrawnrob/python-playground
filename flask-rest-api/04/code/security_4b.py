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
    {
        User(1, 'bob', 'asdf'),
        User(2, 'alice', 'cdfg')
    }
]

username_mapping = {u.username: u for u in users}

# e.g:
# username_mapping['bob']

userid_mapping = {u.id: u for u in users}

# e.g:
# userid_mapping[1]

def authenticate(username, password):
    user = username_mapping.get(username, None)
    # It's best not to compare strings with `==`,
    # as utf8 / unicode characters can give wrong results
    # - However, we can user `safe_str_cmp` for now:
    if user and safe_str_cmp(user.password, password)
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

