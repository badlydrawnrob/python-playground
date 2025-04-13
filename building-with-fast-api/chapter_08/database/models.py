from database.connection import sqlite_db
from peewee import *
from playhouse.sqlite_ext import JSONField

# ------------------------------------------------------------------------------
# PeeWee Data Models (SQLite)
# ==============================================================================
# > The DATA models are thrown together quickly, so this mightn't be the best
# > way to name them, or place them in the app directories.
#
# We could have `data.User` and `api.User` namespaces, but that might look a bit
# ugly when importing. You could also write it like:
#
# ```
# from data.User as D
# from api.User as A
# ```
#
# Notes on SQL terminology
# ------------------------
#
# 1. Understand what a primary key is.
# 2. Understand what a foreign key is.
# 3. Understand what a composite key is.
# 4. Understand what a unique key is.
# 5. Understand what a check constraint is.
# 6. Understand the difference between columns and fields.
#
#
# PeeWee
# ------
# > Different apps do architecture differently.
# > Gmail, for example has a single form for each `User` data point. This might
# > be simpler for a `PATCH`, but it's SO many clicks for the user.
#
# 1. `ID` is automatically created and incremented
# 2. Fields are `null`able by default (add `null=False` to make them required)
# 3. Consider whether data is a `PATCH` or a `PUT`
#    - Does your client want to sent all data or just some?
#    - How will this affect your Elm architecture (forms)?
# 4. Field types that convert into SQLite field types:
#    - @ https://zetcode.com/python/peewee/ (table)
# 5. Field types must be written _with_ the `()` parens, otherwise you're pointing
#    to class type (not instance of class). They should also be
#    allocated as a _variable_ (not with a `:` colon). This is a bit different
#    than SQLModel's Pydantic style fields ...
#    - fieldname = CharField() (correct)
#    - fieldname: CharField (incorrect)
# 6. Backref is set which allows you to access the tweets that refer to a given
#    user. So, rather than running the full query, you can simply write:
#    - @ https://github.com/coleifer/peewee/issues/2027
#    - `user.events` is a shortcut for the full join query. You'll need to have
#      done a `User.create()` or `User.get()` first.
#
# PeeWee extensions
# -----------------
# > @ https://docs.peewee-orm.com/en/latest/peewee/sqlite_ext.html#sqlite-json1
# 
# You could convert a `List String` to a `CharField` string, and then convert
# that with Elm on the client side, but we can use a plugin for SQLite.
#
#
# General info about ORMs
# -----------------------
# It also seems like other ORMs (like PeeWee) require converting from model
# objects (rows) into a dictionary or json structure, but has methods to convert
# the data structures from one form to another. I'm fairly sure FastApi/SQLModel
# has similar, but my early mess around with PeeWee quickstart felt a lot more
# solid than trying to understand how SQLModel types are working.
# 
# @ https://stackoverflow.com/a/21979166 (PeeWee -> dict)
# @ https://tinyurl.com/fastapi-jsonable-convertor (Pydantic -> Json)

class DataModel(Model):
    class Meta:
        database = sqlite_db

class UserData(DataModel):
    #! `ID` is automatically created and incremented
    public = UUIDField(unique=True, null=False)
    email = CharField(unique=True, null=False) # Should be unique!
    password = CharField(null=False)

class EventData(DataModel):
    #! `ID` is automatically created and incremented
    creator = ForeignKeyField(UserData, backref='events')
    title = CharField(null=False)
    image = CharField()
    description = TextField()
    location = CharField()
    tags = JSONField() # `List String`
