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


# Model ------------------------------------------------------------------------

class ToDo(BaseModel):
    id: int
    item: str
