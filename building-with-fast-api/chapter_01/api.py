from fastapi import FastAPI

# ------------------------------------------------------------------------------
# Hello World!
# ==============================================================================
# The most basic route we can make. `app` uses an instance of the `FastAPI` class
# and we return a dictionary. The problem with using the `FastAPI()` instance is
# that it can only run ONE route.
#
# For multiple routes, use the `APIRouter` class.
#
# Running the server
# ------------------
# `uv run uvicorn 01-hello-world.api:app --port 8000 --reload` (from parent dir)

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello World" }
