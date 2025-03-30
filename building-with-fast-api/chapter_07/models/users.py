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
# > We're now using `TokenResponse` instead of `UserSign`, as we use FastApi's
# > own sign-in form setup.
#
# 1. SQLModel doesn't have any `List` types, so we must convert this to a
#    Json field in the database ... it's a list of `Event.id`s.
# 2. When to use `BaseModel` and when to use `SQLModel`?
#    - I really need to figure this out (and the differences)
#    - I have a feeling that `SQLModel` should be used mostly, but if we're simply
#      accessing data from our request body, we can use `BaseModel` too.
# 3. Following from (1) are there any errors using Pydantic for `UserSign`?
#    - This is for sign-up and sign-in, just for testing purposes.
# 4. See `Field()` settings, such as `index=` and `unique=`:
#    - @ ⭐ https://sqlmodel.tiangolo.com/tutorial/indexes/#an-index-and-a-dictionary
#    - @ https://tinyurl.com/pydantic-default-factory (auto-generate)
#    - @ https://github.com/fastapi/sqlmodel/issues/140#issuecomment-950569807 (UUID)
#    - @ https://dev.to/rexosei/how-to-make-a-field-unique-with-sqlmodel-4km9
#
# ⚠️ Warning
# ----------
# > If your `SQLModel` fields are `Optional` it's safe to use as request body,
# > because these fields don't need to be pinged to the API.
#
# 1. Is `default_factory` generated if `User` is used in the request body?!)
#    - This could slow down the function by a few seconds
# 2. Do you _really_ want to make all other fields `Optional`?
#    - This doesn't seem sensible for, say, a user admin area. You'll want to
#      enforce many fields!

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    email: EmailStr # This should be unique (but we're testing in routes already)
    password: str
    events: Optional[List[int]] = Field(sa_column=Column(JSON))
    # events: Optional[List[Event]] # Used to be a list of `Event` types ...

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
