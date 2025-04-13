from pydantic import BaseModel
from typing import List, Optional

# ------------------------------------------------------------------------------
# Our EVENT model (API layer)
# ==============================================================================
# We're not using `SQLModel` anymore! We're using Pydantic's `BaseModel` for any
# incoming request (we could do that for response as well). This keeps the API
# layer and the DATA layer separate. Pydantic fields can be declared in any order.
#
# Questions:
# ----------
# 1. Should fields be named alphabetically or by position? (preference)
# 2. When do we transition to PeeWee's data models?
#
# Using Pydantic
# --------------
# 1. `Optional` is useful when one of the data points isn't required.
# 2. It's easier to NOT nest models (it's errored for me before).
# 3. Some data points need to be handled by PeeWee (like `id`).
# 4. For `EventUpdate`, we could do a `PATCH` or a `PUT` request.
#    - As our example is a `PATCH` request, all fields are optional.
#
# Wishlist
# --------
# > What do we want to leave out and simplify?
#
# 1. The `response_model=` isn't really needed, as we're now using `PeeWee`
#    - But we could use it if we wanted to (and populate the fields)
# 2. Alternatively we could use a response type (the bit after `-> type`)
#    - But is that overkill? Our SQL returns should be predictable!
#    - We could use `TypedDict` to define the response type.
#    - @ https://mypy.readthedocs.io/en/stable/typed_dict.html

class Event(BaseModel):
    id: Optional[int] #! Generate automatically with PeeWee (3)
    creator: Optional[int] #! Create a foreign key with `User.Id` (PeeWee) (3)
    title: str
    image: str
    description: str
    location: str
    tags: List[str]

class EventUpdate(BaseModel):
    # `:id` supplied in the URL
    title: Optional[str]       #! (4)
    image: Optional[str]       #! (4)
    description: Optional[str] #! (4)
    location: Optional[str]    #! (4)
    tags: Optional[List[str]]  #! (4)

class EventJustTitle(BaseModel):
    title: str


# Response Models --------------------------------------------------------------
# > Do we _really_ need typing for our return values?
# > I'm not so convinced it's a good idea!
#
# Our SQL models are already typed, and the return values should be very
# predictable. A `get_user_event() -> dict` could be enough! If we _did_ decide
# to use typing for return values, it'd mean:
#
# 1. Unpacking the `request` type `Event` (Pydantic)
# 2. Calling the database with `EventData` model (PeeWee)
# 3. Convert `EventData` -> `EventWithUser` object ..
# 4. Or, `model_to_dict(event)` and validate it with `response_model=`
#
# That's a lot of work! It makes our code base more complicated. If it were a
# typed functional language, like Elm, then sure. But Python's not that solid
# at typing anyways. You _could_ combine PeeWee and Pydantic, but it feels like
# a lot of work for little gain.
#
# @ https://tinyurl.com/pydantic-peewee-example
#
# ```
# class EventWithUser(BaseModel):
#   pass
# ```
