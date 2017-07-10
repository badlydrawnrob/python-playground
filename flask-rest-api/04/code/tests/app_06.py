from flask import Flask, request
from flask_restful import Resource, Api
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
            return {'message': '{} already exists'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    # Add a delete method
    def delete(self, name):
        # Set a list of all items that are NOT
        # the `name` passed as an argument
        # - Make sure you add a `global` variable
        #   or else, you'll get a "cannot assign
        #   variable" error
        #
        # issues:
        # 1. It doesn't check if the item exists
        # 2. Is there a better way to do this?
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}


class ItemsList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
