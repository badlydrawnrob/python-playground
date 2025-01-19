from fastapi import APIRouter
from model import ToDo

# ------------------------------------------------------------------------------
# A very simple to-do app
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
# > This would make a good "how do we fix this" problem.
#
# 1. Currently if `todo_list` has zero entries, we get an `Internal Server Error`,
#    not our `else` branch from Uvicorn.
#    - `elif` `not []` will return `True` although it feels hacky.
#    - `len([]) == 0` is another option

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
    """Get a single to-do
    
    1. Check if our to-do list is empty
    2. For each to-do, check the `:id`
    3. Print the record if it exists
    """
    if not todo_list:
        return { "message": "Your to-do list is empty" }
    else:
        for todo in todo_list:
            if todo.id == id:
                return { "todo": todo }
            else:
                return {
                    "message": "This to-do doesn't exist!" # (1) !=
                }
