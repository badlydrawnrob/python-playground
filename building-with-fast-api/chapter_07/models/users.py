from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel
from typing import List, Optional
from models.events import Event

# ------------------------------------------------------------------------------
# Our USER model
# ==============================================================================
# See `models.events` for informations and questions on SQLModel.
#
# Questions
# ---------
# 1. When to use `BaseModel` and when to use `SQLModel`?
#    - I really need to figure this out (and the differences)

class User(SQLModel, table=True):
    email: EmailStr # A Pydantic type for emails
    password: str
    events: Optional[List[Event]] # Empty by default, currently not used

# For `sign-up` and `sign-in`
class UserSign(BaseModel):
    email: EmailStr
    password: str
