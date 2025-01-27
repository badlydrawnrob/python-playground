from typing import Annotated

from fastapi import APIRouter, Path
from model import ToDo, Item

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
# Bugs
# ----
# > Think about "how might we fix this" problems for students ...
#
# 1. We're MUTATING the list within this module
#    - This is a problem if we want to use this list elsewhere
#    - We could copy the dictionary if we preferred
#      @ https://tinyurl.com/python-mutable-lists
# 2. `POST` accepts duplicate `{id}`s
# 3. `GET` `{id}` with an `[]` empty `todo_list` returns `Internal Server Error`
#    - Fixed: you can also use `len([]) == 0` here


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
# 2. How can we access to-dos with `.id` dot notation?
# 3. What is an `:id`/`{id}` path?
#    - https://docs.usebruno.com/send-requests/REST/parameters
# 4. What is `Path()` and `Annotated`?
#    - Additional validation (it's a path `:id`), default values, descriptive titles
#    - @ https://tinyurl.com/fastapi-path-params-annotate
# 5. What the fuck is elipsis? (...)
#    - @ https://tinyurl.com/wtf-is-elipsis-python
#
# Wishlist
# --------
# 1. Only partially update `Item` (e.g, the `status` field)
#    - `todo.item.status == str`?
#    - Do we really need another `class` for that?


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


@todo_router.put("/todo/{id}")
async def update_single_todo(
    todo_data: Item,
    id: Annotated[int, Path(title="The ID of the to-do to be updated")] 
    ) -> dict:
    """Update a single to-do
    
    1. Check if the id matches an existing to-do
    2. If exists, replace with request body (`todo_data`)
    3. Return a message if successfully updated
    """
    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data # relace with the request body

            return { "message": "To-do updated successfully" }
        
    return { "message": "To-do with supplied ID doesn't exist" }


@todo_router.delete("/todo/{id}")
async def delete_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to be deleted")]
    ) -> dict:
    """Delete a single to-do
    
    1. Check if the id matches an existing to-do
    2. If exists, remove the to-do
    3. Return a message if successfully deleted
    """
    for todo in todo_list:
        if todo.id == id:
            todo_list.remove(todo)

            return { "message": "To-do deleted successfully" }
        
    return { "message": "To-do with supplied ID doesn't exist" }
