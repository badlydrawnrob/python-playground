from sqlmodel import Column, Field, JSON, SQLModel
from typing import List, Optional

# ------------------------------------------------------------------------------
# Our EVENT model
# ==============================================================================
# We use `SQLModel` rather than Pydantic's `BaseModel` for SQL and tables. It's
# best to be consistent, but Pydantic fields can be declared in any order.
#
# Questions:
# ----------
# 1. What is `session.refresh()` doing? (see `connection.py`)
# 2. Why do we use `table=True`? When can it be omitted?
# 3. What is `sa_column` and what does it do? (or `sa_type`)
#    - @ https://stackoverflow.com/a/70659555
# 4. Should fields be named alphabetically or by position? (preference)
# 5. When is `BaseModel` allowed? (and when is it not?)
#
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
# > FastApi and SQLModel
# 
# 1. `Optional` is useful here when a request body data point isn't required.
#    - But it doesn't mean that the field is optional in the database! `None` and
#      `default=None` is also used. It's important to understand WHY:
#    - @ https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
# 2. Creating connected tables with SQLModel:
#   - @ https://sqlmodel.tiangolo.com/tutorial/connect/create-connected-tables/
# 3. FastApi automatically creates an `id` field if it's left out.
#   - It automatically increments the `id` field.
# 4. `Event.creator` is a foreign key to the `User` table.
#   - Our `authenticate` function returns the `user.email` right now ...
#   - Which is a `String`, but would perform quicker if an `Int` (primary key)
#   - @ @ https://www.dittofi.com/learn/relationships-in-sql-complete-guide-with-examples
# 5. Our `EventUpdate` model is used for _partial_ updates (PATCH).
#   - For that reason, most of the fields are marked as `Optional`.
#   - The client code can be different (some fields required), but we write the
#     model this way for all eventualities. Some fields might be missing!
#   - Different apps do this differently. For example, Gmail has a separate UI
#     form for EACH and EVERY data point in the `User` (name, for example).
#   - This is an app ARCHITECTURE decision.

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # unique identifier
    creator: Optional[str] | None = Field(default=None, foreign_key="user.email") #!
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))

# This isn't a table (it's a type! WITHOUT an `id` field)
class EventUpdate(SQLModel):
    # `:id` supplied in the URL
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]
