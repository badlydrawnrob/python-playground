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
#    - `PUBLIC` id is created (currently) by `nanoid`, so we can't use a
#      `UUIDField()` anymore. We'll use `CHARFIELD()` instead.
#    - You could use `shortuuid` and translate it from/to a `uuid`, but you'd
#      have to do this potentially for every call of `Depends(authenticate)` (or
#      maybe only once, as it's stored in a token)
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
# 7. `ForeignKeyField` uses an `id` (primary key) and I can't seem to find a way
#    to change this behaviour. An `int` is a faster join than a `string` anyway.
#    - `column_name=` is require, as by default PeeWee ads `_id` to field name if
#      it's a foreign key. We'll change it to be the same as book.
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
        # Add strict mode to prevent creating new columns

class UserData(DataModel):
    #! `ID` is automatically created and incremented
    public = TextField(unique=True, null=False) # Was `UUIDField()`
    email = CharField(unique=True, null=False) # Should be unique!
    password = CharField(null=False)

class EventData(DataModel):
    #! `ID` is automatically created and incremented
    creator = ForeignKeyField(UserData, column_name = 'creator', backref='events') #! (7)
    title = CharField(null=False)
    image = CharField()
    description = TextField()
    location = CharField()
    tags = JSONField() # `List String`
