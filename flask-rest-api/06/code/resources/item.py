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
        # You could also use try/except block here
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': '{} already exists'.format(name)}, 400

        data = self.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            ItemModel.insert(item)
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item, 201

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
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item'}, 500
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {'message': 'An error occurred updating the item'}, 500
        return updated_item


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