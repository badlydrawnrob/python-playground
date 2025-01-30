from typing import Annotated, List

from fastapi import APIRouter, Path
from model import ToDo, Item

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
# FastApi types
# -------------
# > See `Annotated` for annotated types.
# > These help us to validate and document our API.
#
# @ https://tinyurl.com/fast-api-import-path
# @ https://stackoverflow.com/a/76399911
# 
#
# Learning points
# ---------------
# > Each chapter has it's own useful learning points that students should know.
#
# 1. By now you should know what a path, request, query is.
# 2. You should understand the difference between mutable and immutable data.
# 3. You should know the difference between `POST`, `GET`, `PUT`, `DELETE`.
# 4. You should know what Pydantic is and how to use it.
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
# `APIRouter()` instead of `FastAPI()` allows us to create multiple routes
# instead of only one!

@todo_router.post("/todo")
async def add_todo(todo: ToDo) -> dict:
    todo_list.append(todo)
    return { "message": "To-do added successfully" }


@todo_router.get("/todo")
async def retrieve_todo() -> List[Item]:
    """Retrieve all to-do items
    
    This is different to the book, as that code doesn't work.
    """
    list = []

    for todo in todo_list:
        list.append(todo.item)

    return list


@todo_router.get("/todo/{id}")
async def retrieve_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to retrieve")]
    ) -> dict:
    """Retrieve a single to-do"""
    if not todo_list: # check if the list is empty
        return { "message": "Your to-do list is empty" }
    else:
        for todo in todo_list:
            if todo.id == id:
                return { "todo": todo }
            else:
                return { "message": f"To-do with (:id {id}) doesn't exist" }


@todo_router.put("/todo/{id}")
async def update_single_todo(
    todo_data: Item,
    id: Annotated[int, Path(title="The ID of the to-do to be updated")] 
    ) -> dict:
    """Update a single to-do"""
    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data # replace with the request body

            return { "message": f"To-do with (:id {id}) updated successfully" }
        
    return { "message": f"To-do with (:id {id}) doesn't exist" }


@todo_router.delete("/todo/{id}")
async def delete_single_todo(
    id: Annotated[int, Path(title="The ID of the to-do to be deleted")]
    ) -> dict:
    """Delete a single to-do

    Uses `.remove()` instead of `.pop()` for readability.
    """
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
