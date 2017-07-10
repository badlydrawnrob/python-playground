'''
Adding/finding our items in the database
'''

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
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        # Item now returns an OBJECT
        # - not a dictionary
        item = ItemModel.find_by_name(name)
        # So we have to pull the variables
        # from the object, and create a dict
        # using our ItemModel.json() method :)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': '{} already exists'.format(name)}, 400

        data = self.parser.parse_args()
        # We can now create an item object,
        # instead of a manual dictionary
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            # And instead of calling the class
            # again (as with a @classmethod),
            # we use a regular method on the
            # new `item` object
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        # Return the dictionary, not the object
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # data['price'], data['store_id'] can be simplified
            # to unpacking the **data
            # - This is safe, so long as we run checks with parser
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        # save the stored item to database
        item.save_to_db()
        # convert object to json
        return item.json()


class ItemsList(Resource):
    def get(self):
        # or: list(map(lambda x: x.json(), ItemModel.query.all()))
        return {'items': [item.json() for item in ItemModel.query.all()]}