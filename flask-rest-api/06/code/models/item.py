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


    ##
    # We change find_by_name() to return an object
    # of type ItemModel, instead of a dictionary
    # - It remains an @classmethod, however
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        # Can be called by
        # - ItemModel.name
        # - ItemModel.price

        if row:
            # Eqivalent of cls(row[0], row[1])
            # - returns ('piano', 17.99)
            # - So .. ItemModel('piano', 17.99)
            return cls(*row)

    ##
    # As each ItemModel is a self contained object
    # that we're creating ... it doesn't make sense for it to
    # be a @classmethod.
    # - It's inserting ITSELF!
    # -- A class method acts independently from the instance
    #    of an object, and as there'll only ever be a single
    #    object we're interested in, we can use a regular function
    ##

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Self is now an object, not a dictionary
        # - We'll pass it with the `data` from the
        #   api json
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()