from pydantic import BaseModel

# ------------------------------------------------------------------------------
# Schema
# ==============================================================================
# ⚠️ Pydantic handles the schema (model) and validation. We can make sure the
# request `POST` request is properly formatted, with specific `key` names;
# making sure all data fields are correct and present.
#
# Problems
# --------
# 1. Any number (including duplicate `id`s)
# 2. Any string (any length, including empty)
#
# Notes
# -----
# 1. Declaration order is important!
#     - Running `uvicorn` with `Item` below `ToDo` throws an error.
# 2. The book uses a `ToDoItem` with `item: str` ...
#     - But we really want to replace the whole `Item`
#     - This keeps the rest of our program consistent!
# 3. You can access attributes by dot notation:
#    - `ToDo().id` or `Item().status`

# Model ------------------------------------------------------------------------
# I'm using Bruno for all examples, which you can see in `/bruno/collection/`
# folder. You can also add model examples as `model_config` that will be used
# in the generated JSON Schema, but it feels messier than splitting out these
# two different concerns.that will be generated in the JSON Schema ..
# but I feel like this is a BAD IDEA and better split out with Bruno.
#
# You can see the alternative route here:
# - @ https://tinyurl.com/py-playground-commit-3ab8420
# - @ https://tinyurl.com/fastapi-json-schema-extra

class Item(BaseModel):
    item: str
    status: str

class ToDo(BaseModel):
    id: int
    item: Item

# class ToDoItem(BaseModel):
#     item: str # update Item
