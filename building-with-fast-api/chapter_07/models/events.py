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
# 3. I'm fairly sure every table needs an `id` field (for unique identifier)
#    - So `Optional` is probably not a good idea
# 4. See `connection.py` for `session.refresh()` information
#
# Questions
# ---------
# > What's the difference between columns and fields?
# > @ https://tinyurl.com/sql-fields-vs-columns
#
# 1. What is `sa_column` and what does it do? (or `sa_type`)
#    - @ https://stackoverflow.com/a/70659555
# 2. If `id` is left out, does FastApi automatically create one?
# 3. Should I name fields alphabetically or by position?
# 4. Could `EventUpdate` just be a `BaseModel`?

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # unique identifier
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
