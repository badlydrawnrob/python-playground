'''
CRUD:
Create, Read, Update, Delete
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
        # Pull out the db query into a
        # separate function ...
        #
        # - You can call this by using `self`
        # - OR `(Classname).find...`
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404


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


    def post(self, name):
        # You can call a classmethod
        # - `Item.find_by_name`
        # - `self.find_by_name`
        if self.find_by_name(name):
            return {'message': '{} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        # Remove the items.append() method
        # - Add in the database method

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

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