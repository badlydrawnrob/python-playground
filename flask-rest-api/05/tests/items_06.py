'''
Adding/finding our items in the database
'''

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    ##
    # Split out the database calls for the
    # - searching for item
    # - adding item
    # - updating item
    ##

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # remember the WHERE clause
        query = "UPDATE items SET price=? WHERE name=?"
        # order is important, same as query
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


    @jwt_required()
    def get(self, name):
        # You could also use try/except block here
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if self.find_by_name(name):
            return {'message': '{} already exists'.format(name)}, 400

        data = self.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        # As there's no way to allow `put()`
        # method to use the `post()` method to create
        # a new item, we'll remove the database
        # connection into a separate class method

        # We also need to make sure if there's an
        # error adding to the database, we catch it.
        # - you could do this anywhere the
        #   database might fail (i.e. `Item.get()`)
        try:
            self.insert(item)
        except:
            # Return a 500 internal server error
            # - 400 = user error
            # - 500 = server error
            return {'message': 'An error occurred inserting the item'}, 500

        return item, 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # REMEMBER to add the `WHERE` clause
        # otherwise it will delete all items
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}


    def put(self, name):
        # Check for correct data
        data = self.parser.parse_args()
        # Use our new class method
        item = self.find_by_name(name)
        # Set the updated method
        updated_item = {'name': name, 'price': data['price']}

        # Try to insert the item,
        # if it doesn't exist
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item'}, 500
        else:
            # Or else, update the item if it does
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred updating the item'}, 500
        return updated_item


class ItemsList(Resource):
    def get(self):
        pass
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * from items"
        # result = cursor.execute(query, )