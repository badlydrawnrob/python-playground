from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # The client should really check if name exists before, so use
        # 400: bad request
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'An item with name {} already exists.'.format(name)}, 400
        else:
            data = request.get_json()
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201  # Created code


class ItemList(Resource):
    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)