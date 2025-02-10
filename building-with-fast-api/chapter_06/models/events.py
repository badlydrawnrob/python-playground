from pydantic import BaseModel
from typing import List

# ------------------------------------------------------------------------------
# Our EVENT model
# ==============================================================================
# Here we'll set our events model, which is linked to `User.Events` table, which
# every user has.

class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

