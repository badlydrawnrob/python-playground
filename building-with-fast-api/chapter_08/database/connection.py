import json
from peewee import *
from logging import getLogger, StreamHandler, DEBUG
from database.settings import Settings

# ------------------------------------------------------------------------------
# Our DATABASE connection
# ==============================================================================
# From here we set up, connect, and open our SQL database to incoming connections.
# You can either have PeeWee setup your database automatically, or do so manually.
# `sqlite:///` url was used for SQLAlchemy, but not it seems for Peewee. See the
# PeeWee docs for advanced database settings.
#
#    @ https://docs.peewee-orm.com/en/latest/peewee/database.html
#
# You can also `.execute_sql` with raw SQL with PeeWee like this:
#
#    @ https://docs.peewee-orm.com/en/latest/peewee/database.html#executing-queries
#
# If you're looking for ASYNC, there's this (old) tutorial, but see also the
# PeeWee GitHub repository for issues on FastApi + PeeWee (the alternative is
# `gevent` or queuing):
#
#    @ https://fastapi.xiniushu.com/uk/advanced/sql-databases-peewee
#    @ https://fastapi.tiangolo.com/async/ (or, just don't use `async` keyword)
#
# Finally, PeeWee uses Active Record style, which is different to SQLAlchemy.
# SQLAlchemy uses Data Mapping style. I don't fully understand the difference,
# but Active Record pattern encapsulates both data and behavior within a single
# object. For CRUD tasks, I don't think the difference really matters much.
#
#    @ https://www.thoughtfulcode.com/orm-active-record-vs-data-mapper/
#
# Basically, the object persists AFTER the `db.close()` connection is closed. I'm
# not sure what repurcusions this would have, as any connection to the route will
# replace the object.
#
# Ideally I'll probably move the whole damn thing into a more Elm-like static
# typed system in the future:
#
#    @ https://aantron.github.io/dream/
#    @ https://discuss.ocaml.org/t/what-is-currently-best-orm-in-ocaml-world/10057
#
#
# Python's quirks
# ---------------
# > Compared to statically typed functional languages ...
#
# 1. A `Person.create()` or `Person.get()` will return an object, whereas in
#    Racket it'd be a `struct`, Elm a `record`. You'd be able to access all
#    key value pairs right away! That's annoying when debugging.
#    - In Python you'd get `<Person: 1>`, or for their `Pet`s, you'd get an
#      object to loop over, `<peewee.ModelSelect object at 0x104261d50>`
#    - You can do `pprint(vars(bob))` but it's ugly as fuck.
#      @ https://stackoverflow.com/a/193539
#
#
# Security
# --------
# 1. We use `.env`ironment variables to store our secrets:
#    - This could be a secret key, API key, etc. Don't hardcode these values,
#      or store them in your GitHub repo!
#    - We can also use it to automatically set the database for local/live
#    - @ https://medium.com/@mahimamanik.22/environment-variables-using-pydantic-ff6ccb2b8976
#
# Wishlist
# --------
# > Currently the data models aren't named very well. Could improve this, but
# > there's a risk that API model names and Data model names clash!
#
# 1. Auto-create the database (similar to the `conn()` function)
# 2. Ask a professional if there's anyway to do a `get_session()` function!
#    - Add this to this package later, if it's possible (commit `1.12.7`)
# 3. Consider connection pooling, too.
# 4. Set SQLite tables to `STRICT` mode (must be performed manually?)
#    - @ https://sqlite.org/stricttables.html
#

# Settings ---------------------------------------------------------------------

settings = Settings()

# Database ---------------------------------------------------------------------
# We're using SQLite here, with settings in our `.env` file.

sqlite_db = SqliteDatabase(
    settings.DATABASE,
    pragmas=json.loads(settings.PRAGMA_SETTINGS),
    autoconnect=False #! Have a professional check this! (1), (2), (3)
    )

# Logging ----------------------------------------------------------------------
# Show SQL queries in the console
# @ https://docs.peewee-orm.com/en/latest/peewee/database.html#logging-queries

logger = getLogger("peewee")
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

# Automatically create database ------------------------------------------------
# How do we do this similar to our `SQLModel` version? (see commit `1.12.4`)

def create_db():
    pass

# Persist the session ----------------------------------------------------------
# Can we persist the session? No examples for PeeWee + FastApi (commit `1.12.4`):
# @ https://docs.peewee-orm.com/en/latest/peewee/database.html#fastapi
# @ https://github.com/fastapi/fastapi/issues/496 (there's many issues on this)
# @ https://fastapi.xiniushu.com/uk/advanced/sql-databases-peewee (old docs)
    
def get_session():
    pass
