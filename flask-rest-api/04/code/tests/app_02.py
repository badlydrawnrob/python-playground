from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# items is an "in memory" datastore,
# so will be cleared when Flask is
# restarted!!
items = []


class Items(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        return {'item': None}, 404

    def post(self, name):
        # When the request is made by
        # the app or Postman, store the json
        # in `data` variable
        # - If the post isn't formatted properly,
        #   `request` will throw an error.
        # - Make sure content-type header is correct!
        data = request.get_json()

        # Change 'price' value to be accessed from
        # the "payload" (stored request)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


# Create a new resource for all items
class ItemsList(Resource):
    # Url doesn't require any params
    def get(self):
        # Return a list of 'items'
        return {'items': items}


api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)
