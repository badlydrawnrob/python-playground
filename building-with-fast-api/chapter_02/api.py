from fastapi import FastAPI
from todo import todo_router

# ------------------------------------------------------------------------------
# A to do app
# ==============================================================================
# Uvicorn cannot use the `APIRouter()` instance directly to serve the application,
# like we did with `uv run uvicorn api:app --port 8000 --reload`. We've got to
# add these routes to the `FastAPI()` instance to enable their visibility.
#
# Include router
# --------------
# `include_router(router, ...)` method is responsible for adding routes defined
# with `APIRouter` class to the main application's instance.
#
# - `app` variable now has an instance of the `FastAPI` class.
# - `.include_router` is a method of this class

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello Buddy!" }

app.include_router(todo_router) # includes TO DO routes (instance of `APIRouter()`)
