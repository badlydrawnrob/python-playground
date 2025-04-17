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
#    - You MUST supply the fallback value, unfortunately ...
#    - @ https://fastapi.tianglo/tutorial/body/ `= None` or `| None = None`
#    - @ https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
#    - @ https://stackoverflow.com/q/76466468 (for the reason why)
# 2. It's easier to NOT nest models (it's errored for me before).
# 3. Some data points need to be handled by PeeWee (like `id`).
#    - For this we MUST provide a default value `None` (though why `Optional`
#      doesn't handle this for us I've no idea) (see (1))
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
    # We automatically generate `id` and `creator` with PeeWee ... (1) (3)
    # - `id` is ommited from the request, as is `creator` (foreign key `User.Id`)
    id: Optional[int] = None # `None` is a fallback value
    creator: Optional[int] = None
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


# Response Models --------------------------------------------------------------
# > What's the benefit of `response_model=` or response types?
#
# Do we _really_ need typing for our return values? I'm not so convinced it's a
# good idea! Where it _is_ useful however, is when you've got sensitive details
# that would otherwise need a lot of manual boilerplate code to remove.
#
# Our SQL models are already typed with PeeWee, so return values should be very
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
# Below is one usecase that could be useful. It removes sensitive `UserData`
# fields from the response. However:
#
#! ⚠️ For some reason `response_model=` doesn't work with `EventWithCreator`.
#! ⚠️ It works if you use it as the _return type_ of the function. So, it might
#! ⚠️ be better to just be explicit and do this manually.
    
class EventJustTitle(BaseModel):
    title: str

class Creator(BaseModel):
    # id: int
    public: str
    email: str
    # password: str

class EventWithCreator(BaseModel):
    # id: int
    creator: Creator
    title: str
    image: str
    description: str
    location: str
    tags: List[str]

