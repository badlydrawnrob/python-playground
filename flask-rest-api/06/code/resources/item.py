'''
Adding/finding our items in the database
'''

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required()
    def get(self, name):
        # Item now returns an OBJECT
        # - not a dictionary
        item = ItemModel.find_by_name(name)
        if item:
            # So we have to pull the variables
            # from the object, and create a dict
            # using our ItemModel.json() method :)
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': '{} already exists'.format(name)}, 400

        data = self.parser.parse_args()
        # We can now create an item object,
        # instead of a manual dictionary
        item = ItemModel(name, data['price'])

        try:
            # And instead of calling the class
            # again (as with a @classmethod),
            # we use a regular method on the
            # new `item` object
            item.insert()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        # Return the dictionary, not the object
        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        # We use `updated_item` object,
        # NOT `item` object, as we want to load
        # the database with NEW data. Otherwise,
        # we'd retrieve the `item` object (with the
        # data from the database, and it wouldn't do
        # anything.
        # - The data we're storing is the `put` request
        #   we've received!
        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred inserting the item'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred updating the item'}, 500
        # Use the json function, as updated_item
        # is now an object
        return updated_item.json()


class ItemsList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({
                'name': row[0],
                'price': row[1]
            })

        connection.close()

        return {'items': items}