from fastapi import APIRouter

# ------------------------------------------------------------------------------
# A very basic setup
# ==============================================================================
# ⚠️ There's no errors or validation here ...
# 
# - This allows ANY dictionary to be sent to the API
# - There's no checks or errors setup

router = APIRouter()


# Model ------------------------------------------------------------------------

todo_list = []


# Routes -----------------------------------------------------------------------
# Here we're using `APIRouter()` instead of `FastAPI()` which allows us to
# create multiple routes instead of only one!
#
# 1. Post a new todo
# 2. Get all todos

@router.post("/todo")
async def add_todo(todo: dict) -> dict:
    todo_list.append(todo)
    return { "message": "Todo added successfully" }

@router.get("/todo")
async def retrieve_todos() -> dict:
    return { "todos": todo_list }
