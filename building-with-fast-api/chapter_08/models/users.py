from pydantic import BaseModel, EmailStr
from sqlmodel import Column, Field, JSON, SQLModel
from typing import List, Optional
from uuid import UUID, uuid4

# ------------------------------------------------------------------------------
# Our USER model
# ==============================================================================
# See `models.events` for information and questions on SQLModel.
#
# Questions
# ---------
# > We're now using `TokenResponse` for our `/signin` route.
#
# 1. There are no `List` types in SQLModel, so we convert this to a JSON field.
#    - We really don't need this list however, as we can use a `join` instead.
# 2. When to use `BaseModel` and when to use `SQLModel`?
#    - I feel that you can use `BaseModel` unless directly working with the
#      database table type (such as `add(Event)` or `delete(Event)`)
#    - `SQLModel` should generally be used (I think)
# 3. See `Field()` settings, such as `index=` and `unique=`:
#    - @ ⭐ https://sqlmodel.tiangolo.com/tutorial/indexes/#an-index-and-a-dictionary
#    - @ https://tinyurl.com/pydantic-default-factory (auto-generate)
#    - @ https://github.com/fastapi/sqlmodel/issues/140#issuecomment-950569807 (UUID)
#    - @ https://dev.to/rexosei/how-to-make-a-field-unique-with-sqlmodel-4km9
#
# ⚠️ Warning
# ----------
# > If your `SQLModel` fields are `Optional` you can safely remove them from the
# > API request body.
#
# 1. I think `default_factory` automatically generates the `UUID` when `.add()`
#    to the database (or when used in the route?)
#    - This slows the main function by a few seconds?
# 2. When using `Optional` fields, are you using `PUT` or `PATCH`? Consider what
#    the user is _doing_, and if fields should be required on the server side
#    (which can be different to the client side):
#    - With `PUT` the whole resource is required!
#    - With `PATCH` you can leave out any field.

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    email: EmailStr # We could force a unique constraint here ...
    password: str
    events: Optional[List[int]] = Field(sa_column=Column(JSON)) #! see `chapter_07`

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
