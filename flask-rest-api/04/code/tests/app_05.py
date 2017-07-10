from flask import Flask, request
from flask_restful import Resource, Api

# Import JWT and our security functions
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'asdf'
api = Api(app)

# Initialise the JWT object
# pass the `security` functions
# - Send it a username and password
#
# 1. authenticate generates the token
# 2. when we send a token, it:
#    - calls the identity function,
#    - checks token
#    - and gets the user id
#    - returning correct user
jwt = JWT(app, authenticate, identity) # /auth

items = []


class Item(Resource):
    # Decorator forces authentication
    # - requires `Authorization` header with JWT token
    @jwt_required()
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
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
