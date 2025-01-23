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
# Unlike Elm lang it seems like _declaration order is important_ here. Running
# `uvicorn` with `Item` below `ToDo` throws an error.

# Model ------------------------------------------------------------------------
# You can also add model examples that will be generated in the JSON Schema ..
# but I feel like this is a BAD IDEA and better split out with Bruno.
# - This is different than the book for Pydantic v2
# - @ https://tinyurl.com/fastapi-json-schema-extra

class Item(BaseModel):
    item: str
    status: str

class ToDo(BaseModel):
    id: int
    item: Item

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "item": {
                        "item": "Grab some shopping for dinner",
                        "status": "to-do"
                    }
                }
            ]
        }
    }
