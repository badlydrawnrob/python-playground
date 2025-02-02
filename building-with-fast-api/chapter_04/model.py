from pydantic import BaseModel
from typing import List

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


# Model ------------------------------------------------------------------------
# To validate our `json` requests.

class ToDo(BaseModel):
    id: int
    item: str

class ToDoItem(BaseModel):
    item: str


# Return type ------------------------------------------------------------------
# To validate our `json` responses (use sparingly)

class ToDoItems(BaseModel):
    todos: List[ToDoItem]
