# ------------------------------------------------------------------------------
# Fruits database models
# ==============================================================================
# > Docs: @ https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/index.html
# > Column types: @ https://github.com/piccolo-orm/piccolo/issues/1257
# > SQL guide: @ https://www.dofactory.com/sql
#
# For full documentation see the `mocking/fruits` example here:
#
#    @ https://github.com/badlydrawnrob/data-playground/tree/master/mocking/fruits
#
#
# Data model
# ----------
# It's best to make sure your DATA model and API model are distinct. Previously
# I used `EventData` and `Event` classes, but Piccolo is a bit better organised.
# Piccolo ORM uses Active Record pattern, rather than Data Mapper (like SQLAlchemy).
#
#
# SQLite and Piccolo
# ------------------
# > ⚠️ `EVENT` is a reserved keyword in SQLite and should not be used as a table
# > name or other identifier without proper "quoting".
#
# 1. Piccolo does not use `STRICT TABLES` by default (SQLite allows anything)[^1]
#     - Values are stored as basic data types: `Integer`, `Real`, `Text`
#     - Insertion values are ordered by class field order (not alphabetically) ...
#     - So be extra careful to validate data with Pydantic before inserting!
#     - PRAGMA settings like `journal_mode=WAL`, `foreign_keys`, `cache_size`,
#       aren't available in Piccolo yet. You can set `TIMEOUT` however.
# 2. All values are optional by default
#     - Can be `None` so be specific with `tables.py`
# 3. `ID`s are auto-incrementing and unique by default (null values are not distinct)
#     - `ID`s are `secret=` by default with API responses, and you can make other
#       values secret in the response if you like.
#     - You can use Piccolo's `create_pydantic_model` or make your own models and
#       exclude secret values there.
# 4. `UUID`s should always be indexed (increases lookup speed) and `NOT NULL`
#     - `UUID` can be shortened for prettier URLs, or use `shortuuid`/nanoid`/`fastnanoid`
#     - Be careful of collisions if you do: https://zelark.github.io/nano-id-cc/
# 5. Always test performance with both `UUID` types and SQL queries ...
#     - But don't overoptimize too early!
#     - `Int` is faster than `bytes`, which is faster than `String` (joins/lookups)
#     - @ https://tinyurl.com/da2acfb-uuid-fast-api-08 (speed testing short UUIDs)
#
#
# [^1]: You can use https://sqlite.org/stricttables.html if you wish, but it limits
#       the range of Piccolo Column types you can use (generally stored as strings
#       or json strings).
#
#
# Piccolo `ForeignKey`
# --------------------
# > Piccolo always joins on any foreign keys, so you can traverse them to get
# > any data field you'd need.
#
# For example: `.where(Event.creator.username == "rob")` to get all events:
#
#    @ https://piccolo-orm.readthedocs.io/en/latest/piccolo/query_types/joins.html#joins
#
#
# Piccolo `BaseUser`
# ------------------
# > By default Piccolo's user management system `/signup` with `username` and
# > `password` only. You can extend it if you prefer.
#
# We're targeting the `ID` field here, but it's probably easier to use `username`,
# as we'd need a `select()` to get the `ID` first. See "Concurrent connections"
# notes below.
#
#
# UUID for security
# -----------------
# > Not strictly necessary (Stackoverflow uses `Serial` IDs), but more secure.
# > Prevents hackers from blitzing by incrementing IDs. Prevents Ai scraping.
#
#
# General SQL notes
# -----------------
# > An ORM and Pydantic handles data conversion for you, whereas with raw SQL you
# > handle the data conversion yourself. FastAPI API response expects a dictionary.
#
# 1. Understand what a primary key is.
# 2. Understand what a foreign key is.
# 3. Understand what a composite key is.
# 4. Understand what a unique key is.
# 5. Understand what a check constraint is.
# 6. Understand the difference between columns and fields.
#
#    @ https://stackoverflow.com/q/11586986 (disadvantages of composite key)
#
#
# Concurrency with read and write
# -------------------------------
# > Piccolo has some issues with SQLite and concurrent connections.
#
# Concurrent connections with SQLite are only an issue if you combine read and
# write operations at the same time. See here for more info:
#
#    @ https://github.com/piccolo-orm/piccolo/issues/1319
#    @ https://piccolo-orm.readthedocs.io/en/1.3.2/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html
#
#
# General architecture notes
# --------------------------
# > A good API book is "APIs you won't hate" by Phil Sturgeon (version 2)
#
# Take care with your endpoints and architecture, think them through on paper
# with the UI in mind. Different apps do architecture differently; Gmail, for
# example has a single form for editing each `User` data point. This makes it a
# little easier to do technically (each is a simple `PATCH`), but results in a
# LOT of clicks for the user.
#
#
# Tooling
# -------
# > Rather than using Piccolo's migrations, we can use `sqlite-utils`.
#
# See the `sqlite_utils.sql` file.
#
#
# Wishlist
# --------
# 1. Which field should `ForeignKey` reference?
#     - `ID` or `username`?
#     - `ID` requires both read and write operations (slower and async issues)
# 2. Many-to-many relationships (tags, categories, etc)
#     - Previous versions this was a `JSONField`

from piccolo.apps.user.tables import BaseUser
from piccolo.table import Table
from piccolo.columns import Array, ForeignKey, Text, UUID, Varchar


class Event(Table):
    """
    We'll use `UUID` instead of auto-incrementing `ID` for more security.

    Piccolo defaults to a `Serial()` auto-incrementing integer primary key, but
    we've changed it to automatically generate a `UUID` for us.
    """
    id = UUID(primary_key=True, index=True)
    creator = ForeignKey(references=BaseUser, target_column=BaseUser.id) #! (1)
    title = Varchar(length=255, null=False)
    image = Varchar(length=255, null=True)
    description = Text() # `None` values allowed
    location = Varchar(length=50, null=True)
    tags = Array(base_column=Varchar(length=50)) #! (2)
