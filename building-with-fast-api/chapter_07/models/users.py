from pydantic import BaseModel, EmailStr
from sqlmodel import Column, Field, JSON, SQLModel
from typing import List, Optional
from uuid import UUID, uuid4

# ------------------------------------------------------------------------------
# Our USER model
# ==============================================================================
# See `models.events` for informations and questions on SQLModel.
#
# Questions
# ---------
# 1. SQLModel doesn't have any `List` types, so we must convert this to a
#    Json field in the database ... it's a list of `Event.id`s.
# 2. When to use `BaseModel` and when to use `SQLModel`?
#    - I really need to figure this out (and the differences)
# 3. Following from (1) are there any errors using Pydantic for `UserSign`?
#    - This is for sign-up and sign-in, just for testing purposes.
# 4. See `Field()` settings, such as `index=` and `unique=`
#    - @ https://sqlmodel.tiangolo.com/tutorial/indexes/#an-index-and-a-dictionary
#    - @ https://tinyurl.com/pydantic-default-factory (auto-generate)
#    - @ https://github.com/fastapi/sqlmodel/issues/140#issuecomment-950569807 (UUID)
#    - @ https://dev.to/rexosei/how-to-make-a-field-unique-with-sqlmodel-4km9

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    email: EmailStr # This should be unique (but we're testing in routes already)
    password: str
    events: Optional[List[int]] = Field(sa_column=Column(JSON))
    # events: Optional[List[Event]] # Used to be a list of `Event` types ...

# (2)
class UserSign(BaseModel):
    email: EmailStr
    password: str
