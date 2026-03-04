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
# SQLite `PRAGMA` settings aren't currently available in Piccolo.
# 
# 
# Timeout
# -------
# > Defaults to `timeout=5` seconds ...
# > Only worry about this if your getting > 30 concurrent users!
# 
# Up to 100 concurrent users with timeout set on ALL THE THINGS helps. Anything
# over 100 users and 10 seconds, you'll get more failures and diminishing returns!
# 10 seconds is also a long time for your users to wait, and it's not going to
# solve the blocking nature of SQLite writes (1 at a time).
# 
# 95% success rate at `-c 100` for `-n 10000` on a single endpoint with the
# timeout set to 10 seconds on all the things. Fewer concurrent users will need
# a shorter timeout:
# 
# - `-t 10s` for Bombardier
# - `timeout=10` for SQLiteEngine()`
# - `timeout_keep_alive=10` for `uvicorn.run`
#
# At this point though, it's better to seek out a professional database or network
# programmer, figure out where your bottlenecks are, and nd a better solution. Failure
# rates can rise to 95%. See the `PERFORMANCE.md` file for more on this. I think
# `SQLiteEngine(timeout=60)` is a wrapper for `sqlite3_busy_timeout()`.
# 
#     @ https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
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

DB = SQLiteEngine(path=DATABASE, log_queries=LOG_QUERIES, log_responses=LOG_RESPONSES, timeout=10)

APP_REGISTRY = AppRegistry(
    apps=["planner.piccolo_app", "piccolo.apps.user.piccolo_app"]
)
