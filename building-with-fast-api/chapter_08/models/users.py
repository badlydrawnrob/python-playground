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
# 3. We're generating a `nanoid` with `default_factory=` automatically. We're now
#     using a shorter code, rather than a long `UUID`. It's very URL friendly.
#    - LOTS of unique ID generators to choose from:
#        - `shortuuid`, `nanoid`, `ksuid` (which can be sorted by generation
#          time), `uuid`, and so on.
#        - Time how long each function runs with the following methods:
#          @ https://builtin.com/articles/timing-functions-python
#    - Make sure to CHECK COLLISIONS (how likely two `nanoid`s will clash?)
#      @ https://zelark.github.io/nano-id-cc/
# 4. Search Brave browser to check how to mark a field as `Optional` but use the
#    default factory pattern: "pydantic mark as optional with default factory"
# 5. We'll leave in `TokenResponse` in for now, which is another example of
#    a `response_model=` or response type. This is our `return` value!
#    - This is used for our `/signin` route.

class User(BaseModel):
    id: Optional[int] #! Generate automatically with PeeWee
    public: UUID = Field(default_factory=uuid4) #! Handled by Pydantic (3), (4)
    email: EmailStr #! This should be unique
    password: str
    # events: Optional[List[int]] #! (1), (2)

class TokenResponse(BaseModel): #! (5)
    access_token: str
    token_type: str
