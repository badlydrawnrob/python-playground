from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, status
from model import ToDo, ToDoItem, ToDoItems

# ------------------------------------------------------------------------------
# A very simple to-do app
# ==============================================================================
# See `chapter_02` and `_03` for full notes.
# Always get a professional to check over your code (for security)
#
# Overview
# --------
# 1. Pydantic helps us validate data
# 2. `/docs` and `/redoc` for documentation (use Bruno!)
# 3. `Annotated` is helpful for auto-generated docs (but I'm not using it)
# 4. `response_model` is a "magic" shortcut (response types are better?)
# 5. Handle errors with `HTTPException` and return the correct `status_code=`
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
# Old Learning points
# -------------------
# > You (the student) should be able to answer ...
#
# 1. What is a: path? request? query?
# 2. What's the difference between mutable and immutable data?
# 3. What is a `POST`, `GET`, `PUT`, `DELETE`? (replace resource or update value?)
# 4. Why is Pydantic useful? How is it used?
#
#
# Wishlist
# --------
# 1. Avoid duplicate `:id`s on `POST`
# 2. Does a request body require `str` length restrictions?
# 3. Make sure `str` length != empty
# 4. Only update the `"item"` _value_ (not the entire thing)
#    - `PUT` -vs- `PATCH` @ https://www.youtube.com/watch?v=s33eVDbsyYM

todo_router = APIRouter()


# Data -------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# We're using Python "magic" in `retrieve_todo`.
# The "Elm way" would be: @ https://tinyurl.com/fast-api-anti-magic-response 

@todo_router.post("/todo", status_code=201)
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
        # currently returns `200` OK: the WRONG status code!
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
        
    raise HTTPException(
        status_code=404,
        detail=f"To-do with (:id {id}) doesn't exist"
    )


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
        
    raise HTTPException(
        status_code=404,
        detail=f"To-do with (:id {id}) doesn't exist"
    )


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    """Delete all to-dos"""
    if not todo_list:
        raise HTTPException(
            status_code=404,
            detail=f"To-do list is empty!"
        )
    else:
        todo_list.clear()
        return { "message": "All to-dos deleted successfully" }
