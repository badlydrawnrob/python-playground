from sqlmodel import Column, Field, JSON, SQLModel
from typing import List, Optional

# ------------------------------------------------------------------------------
# Our EVENT model
# ==============================================================================
# We now use `SQLModel` (or MongoDB) to set our Pydantic models, rather than the
# `BaseModel`. WARNING: remember that this creates a tight coupling between your 
# API and your SQL models, which is not always preferable. This will link to our
# `User.Events` table, for user events.
#
# Questions
# ---------
# > Questions on SQL and the model (how does it look?)
#
# 1. What does `table=` parameter do?
# 2. What does `sa_column=` do?
# 3. What do our fields, such as `id` look like now?
# 4. Is it wise to make `id` column `Optional`? (NO!)
# 5. In which order should fields be? (ABC versus POSITIONAL)
# 6. What is the difference between columns and fields?
#    - @ https://tinyurl.com/sql-fields-vs-columns (dba.stackexchange)
# 7. Does `session` automatically open/close the session?
#    - `.commit()` is responsible for FLUSHING transactions (in the session)

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # unique identifier
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))

# An example database `EventSQL` entry
# new_event = Event(
#     title="Book Launch",
#     image="src/fastapi.png",
#     description="The book launch event will be held at Packt HQ",
#     location="Zoom call",
#     tags=["packt","book"]
# )

# An example database transaction
# session.add(new_event)
# session.commit()

class EventUpdate(SQLModel): # Not a table
    # no id field?
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]
