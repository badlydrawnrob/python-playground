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
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
]

username_mapping = {
    'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

# e.g:
# username_mapping['bob']

userid_mapping = {
    1: {
        'id': 1,
        'username': 'bob'
        'password': 'asdf'
    }
}

# e.g:
# userid_mapping[1]

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

