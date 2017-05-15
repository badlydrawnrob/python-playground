'''
We add in checks to only allow certain json

- reqparse will be deprecated,
  so we need to find an alternative
'''

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'asdf'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'{} already exists'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items

        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # Instantiate the object
        # which we use to parse request
        # - run request through this method
        # - see which arguments match
        parser = reqparse.RequestParser()
        # This can check json payloads
        # AND form payloads
        # - any other json elements will be ignored
        parser.add_argument(
            'price', type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        # Instead of request.get_json()
        # we run the request through the
        # parser!
        data = parser.parse_args()
        # Add another argument, that won't
        # get parsed by reqparse and will
        # throw a `KeyError`.
        # - just to prove it is getting erased
        print(data['another'])

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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
