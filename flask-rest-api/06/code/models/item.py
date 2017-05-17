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

import sqlite3

class ItemModel(object):
    # We need to set this up as
    # every item has an item and a price
    def __init__(self, name, price):
        self.name = name
        self.price = price

    # We also add an representation of
    # the json we'll need
    # - basically a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # Next, add all the methods currently in
    # resources, that are interacting directly
    # with our database (i.e, those that the api
    # doesn't care about ... and add them here
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()