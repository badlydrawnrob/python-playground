# ------------------------------------------------------------------------------
# Piccolo configuration file.
# ==============================================================================
# > @ https://piccolo-orm.com/docs/configuration/
#
# Python decouple
# ---------------
# We can set a default value for production, and make sure the type is set. By
# default `python-decouple` treats values as strings. We've changed from using
# `pydantic-settings` and `peewee` here.
#
#
# Connection to the database
# --------------------------
# > `SQLiteEngine` has no `connect()` and `close()` functions to open/close the
# > `fruits.sqlite` database. You can also add a `timeout=` paramater.
#
# Piccolo handles connections automatically and uses `engine_finder` under the hood
# from this config file. You _may_ need change the transaction type if you're using
# read and write operations together in one endpoint (the database locked issue)
# and concurrent write requests are also problematic at scale (see `app.py` and
# `tables.py` notes for more on this).
#
# Setting `timeout=60` doesn't seem to help much, and anything over this number
# can actually make our timeouts WORSE. I'm unsure why. `SQLiteEngine(timeout=60)`
# is a wrapper for `sqlite3_busy_timeout()`.
#
# SQLite `PRAGMA` settings aren't currently available in Piccolo.
#
#
# ------------------------------------------------------------------------------
# WISHLIST
# ------------------------------------------------------------------------------
# 1. PRAGMAs for SQLite like previous versions?
#     - Especially to reduce `database is locked` concurrent errors
#     - These can be added within `sqlite3` instead of with Piccolo
# 2. Logging for bug-checking with a live API:
#     - @ (article) https://betterstack.com/community/guides/logging/logging-with-fastapi/
#     - @ (previously) https://docs.peewee-orm.com/en/latest/peewee/database.html#logging-queries
#     - `from logging import getLogger, StreamHandler, DEBUG`
#     - Remember that query logs are NOT return values (responses)!

from decouple import config
from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine


DATABASE = config("SQLITE_DATABASE", default="planner.db")
LOG_QUERIES = config("SQLITE_LOG_QUERIES", default=False, cast=bool)
LOG_RESPONSES = config("SQLITE_LOG_RESPONSES", default=False, cast=bool)

DB = SQLiteEngine(path=DATABASE, log_queries=LOG_QUERIES, log_responses=LOG_RESPONSES)

APP_REGISTRY = AppRegistry(
    apps=["planner.piccolo_app", "piccolo.apps.user.piccolo_app"]
)
