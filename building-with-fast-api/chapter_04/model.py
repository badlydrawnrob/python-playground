from pydantic import BaseModel
from fastapi import Form
from typing import List, Optional

# ------------------------------------------------------------------------------
# Schema
# ==============================================================================
# Always prune unused Pydantic schema (model) for validation. Decleration order
# is important, and I've made some slight deviations from the book (on occasion)
# Attributes can be accessed by `.dot` notation!
#
# API documentation
# -----------------
# We're using Bruno instead of `json_schema_extra`. So far it seems like a nicer
# experience and cuts down code (making it more readable). Response data isn't
# documented (yet)
#
# @classmethod
# ------------
# @ https://stackoverflow.com/q/12179271/838046


# Model ------------------------------------------------------------------------
# To validate our `json` requests.

class ToDo(BaseModel):
    id: Optional[int]
    item: str

    @classmethod
    def as_form(cls, item: str = Form()) -> "ToDo":
        return cls(id=None, item=item)

class ToDoItem(BaseModel):
    item: str


# Return type ------------------------------------------------------------------
# To validate our `json` responses (use sparingly)

class ToDoItems(BaseModel):
    todos: List[ToDoItem]
