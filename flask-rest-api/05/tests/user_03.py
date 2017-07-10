'''
Uses `*_02.py` files
'''

import sqlite3
from flask_restful import Resource, reqparse


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
    def find_by_userid(cls, _id):
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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    def post(self):
        # Use __class__ for name?
        data = UserRegister.parser.parse_args()

        # Check if a user already exists
        # - (by username, not user id)
        # - Remember that if we `return` the following code
        #   will not run
        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # The connection must come AFTER the above check,
        # otherwise the connection will never close:
        # - Everything after a `return` statement (if True)
        #   would be ignored
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully'}