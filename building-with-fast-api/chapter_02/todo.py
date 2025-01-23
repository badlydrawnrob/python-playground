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
# FastApi Documentation
# ---------------------
# 👍 API documentation is auto-generated; it uses Swagger and ReDoc:
# - It's not as nice as Bruno, feels a little clunky. Nice to have though!
# - @ http://127.0.0.1:8000/docs/
#
#
# FastApi types
# -------------
# What is `Path`? See also `Annotated`:
#     @ https://tinyurl.com/fast-api-import-path
#     @ https://stackoverflow.com/a/76399911
# 
# ⚠️ Malicious input
# ------------------
# You want to have checks and errors setup to protect yourself, or you a malicious
# user might tank your database!
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
# Here we're using `APIRouter()` instead of `FastAPI()` which allows us to
# create multiple routes instead of only one!
#
# 1. Post a new todo
#    - This requires a _request body_ to be sent to our API.
#    - A request body is simply data you send by `POST`/`UPDATE` etc.
# 2. Get all todos
# 3. Get a particular to-dos (you could List.filter here too)
#    - See Bruno `:id` path @ https://docs.usebruno.com/send-requests/REST/parameters
#    - 🔎 "FastApi Path class" is optional but can be useful for adding additional
#      validation or default values to path parameters.
#    - It's `Path(...,title="descr")` in the book, with elipsis, but here I'm
#      using `Annotated`
#      @ https://tinyurl.com/wtf-is-elipsis-python (seems a dumb idea)
#      @ https://tinyurl.com/fastapi-path-params-annotate

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
