from peewee import *
from logging import getLogger, StreamHandler, DEBUG
from settings import Settings

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
# Security
# --------
# 1. We use an environment variable to store our secrets:
#    - This could be a secret key, API key, etc. Don't hardcode these values,
#      or store them in your GitHub repo!
#    - We can also use it to automatically set the database for local/live
#    - @ https://medium.com/@mahimamanik.22/environment-variables-using-pydantic-ff6ccb2b8976
#
# Wishlist
# --------
# 1. Auto-create the database (similar to the `conn()` function)
# 2. Ask a professional if there's anyway to do a `get_session()` function
# 3. Consider connection pooling, too.
# 4. Set SQLite tables to `STRICT` mode (must be performed manually?)
#    - @ https://sqlite.org/stricttables.html
#


# Database ---------------------------------------------------------------------
# We're using SQLite here, with settings in our `.env` file.

sqlite_db = SqliteDatabase(
    Settings.DATABASE,
    pragmas=Settings.PRAGMA_SETTINGS,
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
