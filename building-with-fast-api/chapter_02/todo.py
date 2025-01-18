from fastapi import APIRouter
from model import ToDo


# ------------------------------------------------------------------------------
# A very to-do app
# ==============================================================================
# You don't want to allow ANY dictionary to be sent to the API, such as
# an empty dict, malformed data, so on. So now we import out model that's been
# set up with Pydantic.
# 
# ⚠️ Malicious input
# ------------------
# You want to have checks and errors setup to protect yourself, or you a malicious
# user might tank your database!
#
# Errors
# ------
# 1. Currently if `todo_list` has zero entries, we get an `Internal Server Error`,
#    not our `else` branch from Uvicorn.

router = APIRouter()


# Data -------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# Here we're using `APIRouter()` instead of `FastAPI()` which allows us to
# create multiple routes instead of only one!
#
# 1. Post a new todo
# 2. Get all todos
# 3. Get a particular todo (you could List.filter here too)
#    - See Bruno `:id` path @ https://docs.usebruno.com/send-requests/REST/parameters
#    - Here we're using 🔎 "FastApi Path class"

@router.post("/todo")
async def add_todo(todo: ToDo) -> dict:
    todo_list.append(todo)
    return { "message": "Todo added successfully" }

@router.get("/todo")
async def retrieve_todos() -> dict:
    return { "todos": todo_list }

@router.get("/todo/{id}")
async def retrieve_single_todo(id: int) -> dict:
    for todo in todo_list:
        # check each dict.id for equality
        if todo.id == id: # The supplied ID in the url
            return {
                "todo": todo # the whole dict
            }
        else:
            return {
                "message": "This To Do doesn't exist!" # (1) !=
            }
