from fastapi import FastAPI
from todo import todo_router

# ------------------------------------------------------------------------------
# A to do app
# ==============================================================================
# See `chapter_02` for full instructions.
# 
# 1. Create routes using the `APIRouter()` class
# 2. Instantiate `FastAPI()` class in `app` ...
# 3. Add the `todo_router` to the `app with `.include_router` method!
#
# Uvicorn
# -------
# `uvicorn api:app --port 8000 --reload`.
#
# Notes
# -----
# > Always authenticate the user.
# > Use a login token and CSRF for forms.
# > Don't share secrets online (Github tokens)
#
# 1. Beware of duplicates and empty lists
# 2. We're using MUTABLE data here (use `.copy()` for immutable?)
# 3. Validate and SANITIZE (malicious input)
# 4. Warn the user of irriversible changes (`DELETE` all)

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello Buddy!" }

app.include_router(todo_router)
