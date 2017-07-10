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
            return {'{} already exists'.format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items

        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    # You can call this method lots of times
    # the output won't change (i.e, you'll
    # only get ONE item, not multiple).
    #
    # So, you can:
    # 1. Create items
    # 2. Update items
    def put(self, name):
        # Get the request
        data = request.get_json()
        # Check if item exists
        item = next(filter(lambda x: x['name'] == name, items), None)
        # 1. If it DOES NOT exist, create it
        #
        # 2. If it DOES exist, use the dictionary
        # `.update()` method:
        #    - adds `key: values`,
        #    - or update if they exist
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        # Make sure you return the item to
        # get a result on Postman/Insomnia!
        # - otherwise you'll get `null`
        return item


class ItemsList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
