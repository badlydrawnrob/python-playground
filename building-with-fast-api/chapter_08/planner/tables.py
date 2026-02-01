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
# > ⚠️ We only have SQL models (not Pydantic `DataIn` validation), which could
# > potentially pollute our database with BAD DATA. SQLite is NOT being run in
# > strict more, so you may want to add a DATA validation layer.
#
# It's best to make sure your DATA model and API model are distinct. Piccolo is
# quite well organised, but you may want to name your models explicitly: `Table`
# for SQL models, and `DataIn`/`ApiIn` validation with Pydantic. Piccolo ORM uses
# the Active Record pattern, rather than SQLAlchemy's Data Mapper.
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
# 2. Column types are required (`null=False`) by default, but ...
#     - `null`` values are not distinct if used
#     - `unique=True` must be used to enforce uniqueness
#     - Foreign key columns are `NULL`able if not explicitly `null=False`
#     - `ID`s auto-increment and are unique/`secret=` by default
#     - Any field can be made `secret=` in API responses (hide it from display)
#     - Pydantic models can be made with `create_pydantic_model`, but generally
#       lean towards bespoke models (and ommit secret fields there)
# 3. `UUID`s and lookup fields should always be indexed and not null
#     - Indexing increases lookup and join speed (`int` > `UUID` > `string`)
#     - Shorten the `UUID` for prettier URLs on the frontend, or replace with a
#       `shortuuid`/nanoid`/`fastnanoid`. It's debatable which method is best.
#     - `UUID` reduces chance of collisions: @ https://zelark.github.io/nano-id-cc/
#     - Is there any benefit in having both `Serial` and `UUID` columns?
#       @ https://github.com/piccolo-orm/piccolo/issues/1271#issuecomment-3395347091
# 4. Always test performance with both `UUID` types and SQL queries ...
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
# SQLite and Async problems
# -------------------------
# > A read and write together in one endpoint can lead to "database locked" error,
# > when performing concurrent requests.
#
#     @ https://piccolo-orm.readthedocs.io/en/latest/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html
#     @ https://github.com/piccolo-orm/piccolo/issues/1319
#
# With atomic inserts/edits you can generally avoid having to worry about this,
# but in cases where it's unavoidable, you'll need an `IMMEDIATE` transaction.
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
# WISHLIST
# --------
# 1. Which field should `ForeignKey` reference?
#     - Should it be `null=False` by default?
#     - We're using `ID` which is a faster lookup ...
#     - But currently have to ping `authenticate()` to get it.
# 2. Many-to-many relationships (tags, categories, etc)
#     - Previous versions this was a `JSONField`

from piccolo.apps.user.tables import BaseUser
from piccolo.table import Table
from piccolo.columns import Array, ForeignKey, Text, UUID, Varchar


class Event(Table):
    """
    We'll use `UUID` instead of auto-incrementing `ID` for more security.

    > Fields are `null=False` by default

    Piccolo defaults to a `Serial()` auto-incrementing integer primary key, but
    we've changed it to automatically generate a `UUID` for us.
    """
    id = UUID(primary_key=True, index=True)
    creator = ForeignKey(references=BaseUser, target_column=BaseUser.id) #! (1)
    title = Varchar(length=255)
    image = Varchar(length=255, null=True)
    description = Text()
    location = Varchar(length=50, null=True)
    tags = Array(base_column=Varchar(length=50), null=True) #! (2)
