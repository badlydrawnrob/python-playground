'''
Main app file (launchable)
'''

# Move some classes to /resources/
# or /models/ packages

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # root folder of project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asdf'
api = Api(app)

# Create database with SQLAlchemy
# - decorator is from Flask
# - SQLAlchemy references our models and generates tables!
#   - Remember to delete and refresh tables when adding new models
#   - Only creates tables that it sees!
#     - Make sure your imports are correct
#       - both this file and resource/models files
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    # Item models will import db also
    # so if we import db from top of file
    # you'll have circular import issue
    # - http://bit.ly/2sSvMpk
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)