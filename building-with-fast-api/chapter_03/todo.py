from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, status
from model import ToDo, ToDoItem, ToDoItems

# ------------------------------------------------------------------------------
# A very simple to-do app
# ==============================================================================
# ⚠️ Beware of malicious code and make sure you sanitize the data (`json`) that
# comes in to the http server. Pydantic helps us validate data. Don't allow anyone
# to tank your database! Have your code checked over by a professional, and make
# sure to use the right tools to protect yourself.
#
#
# API Documentation
# -----------------
# > See Bruno app for all `json` REST examples.
#
# @ http://127.0.0.1:8000/docs/
# @ http://127.0.0.1:8000/redoc/
#
#
# FastApi types etc
# -----------------
# > `Annotated` is helpful with auto-generated docs
# > `response_model` is a "magic" shortcut (if both, `response_model` takes priority)
# >
# > Neither are strictly necessary when using Bruno!
#
# 1. `Annotated` types: help to validate and document API
#    - @ https://tinyurl.com/fast-api-import-path
#    - @ https://stackoverflow.com/a/76399911
# 2. Response types and `response_model=`:
#    - Return the _actual_ type with a response type, which will be used
#      to validate the response. You need to _explicitly_ code the return value.
#    - Use `response_model=` to have FastApi document and validate with
#      a Pydantic model. This is useful when you want to exclude fields.
#    - @ https://fastapi.tiangolo.com/tutorial/response-model/
# 3. Handling errors:
#    - Doesn't exist, protected pages, insufficient permissions, etc
#    - @ https://fastapi.tiangolo.com/tutorial/handling-errors/
#    - @ https://fastapi.tiangolo.com/reference/dependencies/#security
# 
#
# Old Learning points
# -------------------
# > Each chapter has it's own useful learning points that students should know.
#
# 1. By now you should know what a path, request, query is.
# 2. You should understand the difference between mutable and immutable data.
# 3. You should know the difference between `POST`, `GET`, `PUT`, `DELETE`.
# 4. You should know what Pydantic is and how to use it.
#
# New learning points
# -------------------
# - `PUT` replaces the resource (e.g: the whole record)
# - `PATCH` replaces the _value_ (e.g: `{ "name": "new product name" }`)
# - `HTTPException` tells our client what went wrong (with correct status code)
#
#
# Wishlist
# --------
# 1. Duplicate `:id`s should not be allowed
# 2. String length: how long?
# 3. String length: not empty
# 4. Only partially update `Item` (e.g, the `status` field)

todo_router = APIRouter()


# Data -------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# We're using Python "magic" in `retrieve_todo`.
# The "Elm way" would be: @ https://tinyurl.com/fastapi-anti-magic-responsel 

@todo_router.post("/todo")
async def add_todo(todo: ToDo) -> dict:
    todo_list.append(todo)
    return { "message": "To-do added successfully" }

# Return the ToDo list without the `:id`
@todo_router.get("/todo", response_model=ToDoItems)
async def retrieve_todo() -> dict:
    return { "todos": todo_list }


# Return the ToDo _with_ the `:id`
@todo_router.get("/todo/{id}")
async def retrieve_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to retrieve")]
    ) -> dict:

    if not todo_list: # check if the list is empty
        return { "message": "Your to-do list is empty" }
    else:
        for todo in todo_list:
            if todo.id == id:
                return { "todo": todo }
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"To-do with (:id {id}) doesn't exist"
                )


# Update a single ToDo (the first one it finds)
@todo_router.put("/todo/{id}")
async def update_single_todo(
    todo_data: ToDoItem,
    id: Annotated[int, Path(title="The ID of the to-do to be updated")]
    ) -> dict:

    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data.item # replace with the request body

            return {
                "message": f"To-do with (:id {id}) updated successfully",
                "todos": todo_list #! Debugging (don't do this in production!)
            }
        
    return { "message": f"To-do with (:id {id}) doesn't exist" }


# Delete a single ToDo
@todo_router.delete("/todo/{id}")
async def delete_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to be deleted")]
    ) -> dict:
    """Uses `.remove()` instead of `.pop()` for readability."""

    for todo in todo_list:
        if todo.id == id:
            todo_list.remove(todo) # remove the to-do

            return { "message": f"To-do with (:id {id}) deleted successfully" }
        
    return { "message": f"To-do with (:id {id}) doesn't exist" }


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    """Delete all to-dos"""
    if not todo_list:
        return { "message": "Your to-do list is already empty" }
    else:
        todo_list.clear()
        return { "message": "All to-dos deleted successfully" }
