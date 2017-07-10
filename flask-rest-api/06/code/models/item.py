'''
As we're only using these
item methods internally (apps interacting
with the api don't care about them)
- They don't change the api
- They only interact with our database
- So we move them to /models/items
'''

##
# The item model only cares about itself
# - So we can directly test it by submitting
#   raw data
##

from db import db

# Extend db.model

class ItemModel(db.Model):
    # SQLAlchemy variables
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Add a store variable
    # - Matches the stores id
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Link to one store only
    # - SQLite DOES NOT enforce relationships,
    #   so you could create this even though a store doesn't exist
    #   - Create a store first ...
    #   - Or use PostgreSQL which enforces keys
    store = db.relationship('StoreModel')

    # We need to set this up as
    # every item has an item and a price
    def __init__(self, name, price, store_id):
        # Variable names must be same as SQLAlchemy
        self.name = name
        self.price = price
        self.store_id = store_id

    # We also add an representation of
    # the json we'll need
    # - basically a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # We change find_by_name() to return an object
    # of type ItemModel, instead of a dictionary
    # - It remains an @classmethod, however

    @classmethod
    def find_by_name(cls, name):
        # Equivalent of: SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()