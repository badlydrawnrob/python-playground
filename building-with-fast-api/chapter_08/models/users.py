from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID, uuid4

# ------------------------------------------------------------------------------
# Our USER model
# ==============================================================================
# See `models.events` for information and questions on Pydantic.
#
# Using Pydantic
# --------------
# 1. Some APIs have a `List ID`, such as `List Image`, for example:
#    - This depends on the app architecture, and if it's a public API. A list
#      of images would help you `andThen` grab each `/image/{id}` route.
#    - As we don't have a public API, we can leave this out ...
#    - And use a `join` on the `Event` table instead!
# 2. If we decided to use a `List[str]` here, it could be a `json` blob!
#    - For that though, PeeWee would need to use an SQLite extension.
#    - Better to use data normalisation where possible.
# 3. `default_factory=` will automatically generate a new `UUID`.
#    - @ Brave "pydantic mark as optional but default factory"
# 4. We'll leave in `TokenResponse` in for now, which is another example of
#    a `response_model=` or response type. This is our `return` value!
#    - This is used for our `/signin` route.

class User(BaseModel):
    id: Optional[int] #! Generate automatically with PeeWee
    public: UUID = Field(default_factory=uuid4) #! Handled by Pydantic (3)
    email: EmailStr #! This should be unique
    password: str
    # events: Optional[List[int]] #! (1), (2)

class TokenResponse(BaseModel): #! (4)
    access_token: str
    token_type: str
