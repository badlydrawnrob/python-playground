'''
We're allowing the user class to interact
with sqlite, creating user mappings (similar
to the functions we created in `security.py`
`usename_mapping`, `userid_mapping`)
'''

import sqlite3


class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # Find user by username in database
    # - Make this a class method as it's not an
    #   instance method
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Setup the query with a placeholder
        query = "SELECT * FROM users WHERE username=?"
        # Store the result
        # - using a single tuple, 'username'
        #   - MUST be a tuple
        result = cursor.execute(query, (username,))
        # Return the first row out of
        # `result` set
        # -
        row = result.fetchone()
        # `row` will return `None` if no `result`
        # so we need to check if exists
        if row:
            # 1. Instead of hardcoding the Class
            #    - User(row[0] ...
            # We can use `cls` (Python convention)
            #
            # 2. Instead of row[0], row[1], row[2]
            # - we can unpack the tuple `*row`
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    # Create a class method exactly the same
    # as the one above, but for the ID
    # - Remember, we're using `_id` with an
    # underscore to avoid naming conflicts with Python
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
