from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates

from model import ToDo, ToDoItem, ToDoItems

# ------------------------------------------------------------------------------
# A very simple to-do app
# ==============================================================================
# 🚀 See @ commit `1.8.1` for `json` only version (without Jinja templates)
# 
# I've CUT CODE DOWN! @ https://tinyurl.com/cutcodedown-com-minimalist and am
# not using `/doc` or `/redoc` (much) whose `Annotated[]` and other code just
# adds needless complexity (and lessens readability). Just use Bruno for now.
# 
#
# Overview
# --------
# > See `chapter_02` and `_03` for full notes.
# > Always get a professional to check over your code (for security)
#
# 1. Pydantic helps us validate data
# 2. `/docs` and `/redoc` for documentation (use Bruno!)
# 3. `Annotated` is helpful for auto-generated docs (but I'm not using it)
#     - #! It is useful for adding contstraints, however (min/max length)
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
# New learning points
# -------------------
# > ⚠️ Jinja could be useful for SMALL bits of html, but as it scales this
# > setup would become unwieldy and unreadable. Jinja temlates are quite 
# > simple and have `if`, loops, flters, functions, etc.
#
# 1. The book uses Bootstrap framework, but I'll use Pico CSS.
# 2. You'll need to understand `Request` and `Depends` for Jinja templates.
#    - @ https://fastapi.tiangolo.com/advanced/using-request-directly/
#    - @ https://tinyurl.com/fastapi-what-is-depends
#    - @ https://fastapi.tiangolo.com/tutorial/request-forms/#about-form-fields
# 3. `.TemplateResponse()` and `.as_form` methods
#    - These are fairly self-explanatory but unusual compared to Elm.
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

# Templates --------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")


# Routes -----------------------------------------------------------------------
# We're using Python "magic" in `retrieve_todo`.
# The "Elm way" would be: @ https://tinyurl.com/fast-api-anti-magic-response 

@todo_router.post("/todo", status_code=201)
async def add_todo(request: Request, todo: ToDo = Depends(ToDo.as_form)):
    for item in todo_list:
        if item.id == todo.id:
            raise HTTPException(
                status_code=409,
                detail="To-do with id already exists"
            )

    todo.id = len(todo_list) + 1 # increment the `:id`
    todo_list.append(todo) # add the new to-do

    return templates.TemplateResponse("todo.jinja", {
        "request": request,
        "todos": todo_list
    })


# Return the ToDo list without the `:id`
@todo_router.get("/todo", response_model=ToDoItems)
async def retrieve_todo(request: Request) -> dict:
    return templates.TemplateResponse("todo.jinja", {
        "request": request,
        "todos": todo_list
    })


# Return the ToDo _with_ the `:id`
@todo_router.get("/todo/{id}")
async def retrieve_single_todo(request: Request, id: int):

    if not todo_list:
        raise HTTPException(status_code=404, detail="To-do list is empty!")
    else:
        for todo in todo_list:
            if todo.id == id:
                return templates.TemplateResponse("todo.jinja", {
                    "request": request,
                    "todo": todo
                })
                    
        raise HTTPException(
            status_code=404,
            detail=f"To-do with (:id {id}) doesn't exist"
        )


# Update a single ToDo (the first one it finds)
@todo_router.put("/todo/{id}")
async def update_single_todo(todo_data: ToDoItem, id: int) -> dict:

    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data.item # replace with the request body

            return { "message": f"To-do with (:id {id}) updated successfully" }
        
    raise HTTPException(
        status_code=404,
        detail=f"To-do with (:id {id}) doesn't exist"
    )


# Delete a single ToDo
@todo_router.delete("/todo/{id}")
async def delete_single_todo(id: int) -> dict:
    """Uses `.remove()` instead of `.pop()` for readability."""
    for todo in todo_list:
        if todo.id == id:
            todo_list.remove(todo)

            return { "message": f"To-do with (:id {id}) deleted successfully" }
        
    raise HTTPException(
        status_code=404,
        detail=f"To-do with (:id {id}) doesn't exist"
    )


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    """Delete all to-dos
    
    The `if` isn't entirely necessary here
    """
    if not todo_list:
        raise HTTPException(
            status_code=404,
            detail=f"To-do list is already empty!"
        )
    else:
        todo_list.clear()
        return { "message": "All to-dos deleted successfully" }
