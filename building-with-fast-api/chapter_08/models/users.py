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
# 1. ⭐ There are no `List` types in SQLModel, so in `chapter_07` we used JSON field.
#    - However, we REALLY DON'T NEED this list in our `User` model. Use a join!
#    - Working with `JSON` data is a pain, and we need to use `JSONB` instead,
#      but the ORMs make this tricky to work with. Much easier with raw SQL. See
#      our WISHLIST in `main.py` for more details.
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
    #! See `chapter_07` and `Q1` for more info
    #! events: Optional[List[int]] = Field(sa_column=Column(JSON))

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserProfile(SQLModel):
    id: UUID
    email: EmailStr
    title: str
