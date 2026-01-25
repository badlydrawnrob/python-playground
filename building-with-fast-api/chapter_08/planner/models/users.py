# ------------------------------------------------------------------------------
# Our USER model (API layer)
# ==============================================================================
# Seem `planner.models.events` for documentation on how to use Pydantic.
#
# Pydantic
# --------
# > Our JWT holds some data about the user, which we can retrieve and format
# > as a Pydantic model.
#
# `TokenResponse` can be added to the `response_model=` or `-> ResponseType`. It
# is only used for our `/signin` route.
#
# Pydantic will automatically check `EmailStr` is valid, but the `email-validator`
# package must be installed.
#
# WISHLIST
# --------
# 1. #! Should we have a list of `Event` IDs on the `User` model?
#     - Is this the way they've got it in the book?

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """ User model for incoming requests.
    
    Piccolo will automatically handle the `ID` field (which is an indexed `UUID`).
    See `planner.models.tables.py` for unique constraints etc.
    """
    username: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
