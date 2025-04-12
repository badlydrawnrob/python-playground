from database.connection import sqlite_db
from peewee import *
from playhouse.sqlite_ext import JSONField

# SQLite (general info)
# ---------------------
# > Terminology
#
# 1. Understand what a primary key is.
# 2. Understand what a foreign key is.
# 3. Understand what a composite key is.
# 4. Understand what a unique key is.
# 5. Understand what a check constraint is.
# 6. Understand the difference between columns and fields.
#
# PeeWee
# ------
# > Different apps do architecture differently.
# > Gmail, for example has a single form for each `User` data point.
# > This might be simpler for a `PATCH`, but it's SO many clicks for the user.
#
# 1. `ID` is automatically created and incremented
# 2. Consider whether data is a `PATCH` or a `PUT`
#    - Does your client want to sent all data or just some?
#    - How will this affect your Elm architecture (forms)?
# 3. Field types that convert into SQLite field types:
#    - @ https://zetcode.com/python/peewee/ (table)
# 4. Field types must be written _with_ the `()` parens, otherwise you're pointing
#    to class type (not instance of class). They should also be
#    allocated as a _variable_ (not with a `:` colon). This is a bit different
#    than SQLModel's Pydantic style fields ...
#    - fieldname = CharField() (correct)
#    - fieldname: CharField (incorrect)
#
# unique constraint on the email field
#
# > Peewee SQLite extensions
# > @ https://docs.peewee-orm.com/en/latest/peewee/sqlite_ext.html#sqlite-json1
# 
# You could convert a `List String` to a `CharField` string, and then convert
# that with Elm on the client side, but we can use a plugin for SQLite.
#
#
# It also seems like other ORMs (like PeeWee) require converting from model
# objects (rows) into a dictionary or json structure, but has methods to convert
# the data structures from one form to another. I'm fairly sure FastApi/SQLModel
# has similar, but my early mess around with PeeWee quickstart felt a lot more
# solid than trying to understand how SQLModel types are working.
# 
# @ https://stackoverflow.com/a/21979166 (PeeWee -> dict)
# @ https://tinyurl.com/fastapi-jsonable-convertor (Pydantic -> Json)
#
# > `null` is on by default for fields
#
# Wishlist
# --------
# > By default PeeWee only supports certain data types
# > You'll need to use a plugin to support JSON blobs.
#
# 1. You'll need `SqliteExtDatabase` for `List[str]` and `JSONField`
#    - @ https://docs.peewee-orm.com/en/latest/peewee/sqlite_ext.html
#    - @ https://docs.peewee-orm.com/en/latest/peewee/sqlite_ext.html#sqlite-json1

class DataModel(Model):
    class Meta:
        database = sqlite_db

class User(DataModel):
    #! `ID` is automatically created and incremented
    public = UUIDField(unique=True, null=False)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)

class Event(DataModel):
    #! `ID` is automatically created and incremented
    creator = ForeignKeyField(User, backref='event')
    title = CharField(null=False)
    image = CharField()
    description = TextField()
    location = CharField()
    tags = JSONField() # `List String`
