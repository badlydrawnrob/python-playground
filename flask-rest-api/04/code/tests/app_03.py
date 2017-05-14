from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        # Same as our previous loop:
        # searches all 'name' values and returns
        # matching value.
        #
        # `next()` gives us the first item returned by
        # filter:
        # - We should probably check on `post()` creation
        #   if a `name` already exists to avoid duplicates
        # - `next() also allows us to return a default
        #   if not found :)
        #
        # Item will return the dictionary we want, or None

        item = next(filter(lambda x: x['name'] == name, items), None)

        # We use a ternary operator to give the correct
        # header response code:
        # - You could also use `if item is not None`
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # Now, add a check to see if the item already
        # exists ...
        # - 400 is response header for bad request
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'An item with name {} already exists'.format(name)}, 400
        # If it doesn't, continue ...
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
