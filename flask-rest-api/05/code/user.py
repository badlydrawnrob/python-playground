import sqlite3

# Allow user class to interact with sqlite
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
            # Instead of hardcoding the Class
            # - User(row[0] ...
            # use `cls`
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user
