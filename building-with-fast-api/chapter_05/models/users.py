from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event

# ------------------------------------------------------------------------------
# Our USER model
# ==============================================================================
# ~~Here we'll set our user model, which has a `User.Events` column, to list all
# the events attached to that specific user. We have a couple of types, depending
# on the situation (for example, sign-in form).~~ We could also create a separate
# `User` model for the `response_model=` in our routes, to hide the `password`.
#
# Questions
# ---------
# 1. Will `Optional` give us a `null` in the `json` output?
# 2. Can we inherit from another custom class? i.e: `UserTwo(User)`?
#    - This seems possible but error prone.

class User(BaseModel):
    email: EmailStr # A custom type for emails
    password: str
