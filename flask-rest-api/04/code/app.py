from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Items(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name, 'price': 12.99}
        items.append(item)
        return item, 201


api.add_resource(Items, '/item/<string:name>')

app.run(port=5000, debug=True)
