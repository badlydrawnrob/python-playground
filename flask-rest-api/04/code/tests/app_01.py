from flask import Flask
from flask_restful import Resource, Api

# As we're using `flask_restful`,
# we no longer need to use jsonify,
# we can use regular dictionaries

app = Flask(__name__)
api = Api(app)

# Create an empty dict
items = []


# Create a resource,
# extending `Resource` class
class Item(Resource):
    # `name` as an argument
    def get(self, name):
        # Loop through and find item
        for item in items:
            # If a 'name' key matches
            # `name` value (e.g. piano)
            if item['name'] == name:
                # Return item if exists
                return item
        # Else, return nothing (in json)
        # - also return `404` not found
        return { 'item': None }, 404

    # post using the same `name` variable
    def post(self, name):
        # Create the item with
        # `key: value` pairs
        item = {'name': name, 'price': 12.00}
        items.append(item)
        # Also return the json
        # - `201` means item created
        return item, 201

# Resource must be added to work
# - along with the url we'll `post` or `get`
api.add_resource(Item, '/item/<string:name>')

# Run the app
app.run(port=5000, debug=True)
