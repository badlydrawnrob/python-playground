'''
Allow users to sign up
'''

import sqlite3
from flask_restful import Resource, reqparse


# User class must not be the same as the
# resource we're using to sign up!

class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


# Add user signup to the api (flask_restful)
class UserRegister(Resource):
    # Add checks for data receivable
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    # You DO NOT need parameters `username`
    # or `password` in the post(params)
    # - We pull it in from the json received!!
    #   `data` object analyses the json
    def post(self):
        # Add the parsing object with classname
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Because our `create_table.py` has
        # `id` as auto-increment, we need to pass
        # `NULL` as the first tuple item
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # Needs to be a tuple
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully'}, 201