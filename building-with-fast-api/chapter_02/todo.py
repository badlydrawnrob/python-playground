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

router = APIRouter()


# Data -------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# Here we're using `APIRouter()` instead of `FastAPI()` which allows us to
# create multiple routes instead of only one!
#
# 1. Post a new todo
# 2. Get all todos

@router.post("/todo")
async def add_todo(todo: ToDo) -> dict:
    todo_list.append(todo)
    return { "message": "Todo added successfully" }

@router.get("/todo")
async def retrieve_todos() -> dict:
    return { "todos": todo_list }
