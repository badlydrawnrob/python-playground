from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import

# We're adding a token here with flask_jwt
# - The user sends us their details,
# - We send them a token to use for their session

app = Flask(__name__)
app.secret_key = 'asdf' # This should be secure
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'An item with name {} already exists'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemsList(Resource):
    def get(self):
        return {'items': items}, 201


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
