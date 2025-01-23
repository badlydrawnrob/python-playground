from typing import Annotated

from fastapi import APIRouter, Path
from model import ToDo

# ------------------------------------------------------------------------------
# A very simple to-do app
# ==============================================================================
# You don't want to allow ANY dictionary to be sent to the API, such as
# an empty dict, malformed data, so on. So now we import out model that's been
# set up with Pydantic. FastApi and Pydantic also help to document our API endpoints,
# and Bruno helps us test it.
#
#
# API Documentation
# -----------------
# 👍 API documentation is auto-generated; the single most useful thing here is
# probably the OpenApi `.json` file, which can be imported online, used in apps,
# or shared with other devs ... it uses Swagger and ReDoc:
# -  @ http://127.0.0.1:8000/docs/
# -  @ http://127.0.0.1:8000/redoc/
# 
# 👎 It's NOT as nice as Bruno, ui feels a little clunky. At some stage you might
# be able to sync the OpenApi `.json` file into this app.
# - @ https://github.com/usebruno/bruno/issues/81
#
#
# FastApi types
# -------------
# What is `Path`? See also `Annotated`:
#     @ https://tinyurl.com/fast-api-import-path
#     @ https://stackoverflow.com/a/76399911
# 
#
# ⚠️ Malicious input
# ------------------
# You want to have checks and errors setup to protect yourself, or you a malicious
# user might tank your database!
#
#
# Fixing Errors
# -------------
# > This would make a good "how do we fix this" problem.
#
# 1. Now we're giving an error message if `todo_list` contains zero entries.
#    - Otherwise we'll get a `Internal Server Error`
#    - `len([]) == 0` is another way to do this

todo_router = APIRouter()


# Data -------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# See `/docs` or `/redoc` (urls), or `/bruno` (folder) for documentation!
# 
# Here we're using `APIRouter()` instead of `FastAPI()` which allows us to
# create multiple routes instead of only one!
#
#
# Useful knowledge ...
# --------------------
# 1. What is a _request body_?
# 2. What is an `:id`/`{id}` path?
#    - https://docs.usebruno.com/send-requests/REST/parameters
# 3. What is `Path()` and `Annotated`?
#    - Additional validation, default values, descriptive titles
#    - @ https://tinyurl.com/fastapi-path-params-annotate
# 4. What the fuck is elipsis? (...)
#    - @ https://tinyurl.com/wtf-is-elipsis-python

@todo_router.post("/todo")
async def add_todo(todo: ToDo) -> dict:
    todo_list.append(todo)
    return { "message": "To-do added successfully" }

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return { "todos": todo_list }

@todo_router.get("/todo/{id}")
async def retrieve_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to retrieve")]
    ) -> dict:
    """Get a single to-do
    
    1. Check if our to-do list is empty
    2. For each to-do, check the `:id`
    3. Print the record if it exists
    """
    if not todo_list:
        return { "message": "Your to-do list is empty" } # (1) !=
    else:
        for todo in todo_list:
            if todo.id == id:
                return { "todo": todo }
            else:
                return { "message": "This to-do doesn't exist" }
