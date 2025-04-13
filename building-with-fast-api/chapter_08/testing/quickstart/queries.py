from peewee import *
from people as p

# ------------------------------------------------------------------------------
# Renaming modules
# ==============================================================================
# Using the `from people as p` renaming syntax doesn't highlight the write
# colours. It sucks. Probably use `PersonData` and rename the table name.
# Or maybe I just can't figure it out ... it's easy peasy in Elm.

p.sqlite_db.connect()
people = p.Person.select()
list = [person.name for person in people]
print(list)
db.close()
