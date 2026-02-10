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
# Notes
# -----
# 1. Remember that query logs are NOT return values (responses)!
# 2. `SQLiteEngine(timeout=60)` is a wrapper for `sqlite3_busy_timeout()`
#     - Setting to 60 doesn't seem to help very much ...
#     - Setting to more than 60 seems to give MORE timeouts!
# 3. SQLite `PRAGMA` settings aren't currently available in Piccolo.
#
# Wishlist
# --------
# 1. PRAGMAs for SQLite like previous versions?
#     - Especially to reduce `database is locked` concurrent errors.
# 2. Logging for bug-checking with a live API:
#     - @ (article) https://betterstack.com/community/guides/logging/logging-with-fastapi/
#     - @ (previously) https://docs.peewee-orm.com/en/latest/peewee/database.html#logging-queries
#     - `from logging import getLogger, StreamHandler, DEBUG`

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
