from sqlmodel import Column, Field, JSON, SQLModel
from typing import List, Optional

# ------------------------------------------------------------------------------
# Our EVENT model
# ==============================================================================
# We use `SQLModel` rather than Pydantic's `BaseModel` when we're dealing with
# database tables (CRUD). Some people say tightly coupling your API and SQL models
# is a bad idea, but will stick with it for now.
#
# Notes
# -----
# 1. Pydantic fields can be any order (as they're named arguments)
# 2. `table=True` is used to create a table in the database
# 3. See `connection.py` for `session.refresh()` information
#
# SQL: general
# ------------
# 1. Does every table need a primary key, or `id` field? (unique identifier)
#    - So `Optional` is probably not a good idea
# 2. Creating connected tables with SQLModel:
#    - @ https://sqlmodel.tiangolo.com/tutorial/connect/create-connected-tables/
# 3. Does FastApi automatically create an `id` field if it's left out?
#    - Does it automatically create a primary key?
#    - Does it auto-increment?
#    - @ ⭐ https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
#      this is useful to understand: why `default=None`?
# 4. #! Currently the `creator` is just a string, which we've converted to a
#    foreign key. Our `/auth` function returns a `user.email`, so we'll use that.
#    - Ideally the `User.id` field (UUID) would be used instead!
#    - @ https://www.dittofi.com/learn/relationships-in-sql-complete-guide-with-examples
#
# Questions
# ---------
# > What's the difference between columns and fields?
# > @ https://tinyurl.com/sql-fields-vs-columns
#
# 1. What is `sa_column` and what does it do? (or `sa_type`)
#    - @ https://stackoverflow.com/a/70659555
# 2. Should I name fields alphabetically or by position?
# 3. Could `EventUpdate` just be a `BaseModel`?

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # unique identifier
    creator: Optional[str] | None = Field(default=None, foreign_key="user.email") #!
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))

# This is a type, not a table!
class EventUpdate(SQLModel):
    # ID Field not required (supplied in `:id` url)
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]
