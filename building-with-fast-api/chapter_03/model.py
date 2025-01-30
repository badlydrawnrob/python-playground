from pydantic import BaseModel
from typing import List

# ------------------------------------------------------------------------------
# Schema
# ==============================================================================
# ⚠️ Pydantic for schema (model) and validation. Prune anything that isn't used.
#
# Notes
# -----
# 1. Decleration order is important!
#     - Running `uvicorn` with `Item` below `ToDo` throws an error.
# 2. Slight deviations from the book (where it makes sense).
# 3. You can access attributes by dot notation.
#
# Bruno
# -----
# We'll use Bruno instead of `model_config` within the `class`es. It's a far nicer
# experience to view the documentation there. See `/chapter_02` for more info.
#
# - Our response data won't have examples with Bruno.
# - You can figure it out by looking at the `json` responses.


# Model ------------------------------------------------------------------------
# These are what we'll use to validate our `json` requests.

class Item(BaseModel):
    item: str
    status: str

class ToDo(BaseModel):
    id: int
    item: Item

# Return type ------------------------------------------------------------------
# These are what we'll use to validate our `json` responses.
