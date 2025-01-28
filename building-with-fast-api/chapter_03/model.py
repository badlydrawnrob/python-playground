from pydantic import BaseModel

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
# See Bruno folder for all `json` REST examples. The book uses in-place schemas
# but I find them ugly and it's better to seperate concerns. See `chapter_02` for
# more information.


# Model ------------------------------------------------------------------------

class Item(BaseModel):
    item: str
    status: str

class ToDo(BaseModel):
    id: int
    item: Item
