'''
Our launchable app file
'''

# Removed `request, `Resource`, `jwt_required`, `reqparse`
# - we'll import them in `items_04.py`

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from items import Item, ItemsList

app = Flask(__name__)
app.secret_key = 'asdf'
api = Api(app)
jwt = JWT(app, authenticate, identity)

##
# REMOVE items functions, and empty list
# - moved to own file and will store in database!
##

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

# Make sure we only run the app if
# callling the file via `python app.py`
# - `__main__` is the file you "run"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
