'''
We're now adding/loading items from the database
- uses previous versions of files
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

    @jwt_required()
    def get(self, name):
        # Set up the connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Set up the query and find the result
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        # Store the result in `row`
        row = result.fetchone()
        # Close the db connection
        connection.close()

        # Check if `row` contains a result
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'{} already exists'.format(name)}

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


    def delete(self, name):
        global items

        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemsList(Resource):
    def get(self):
        return {'items': items}