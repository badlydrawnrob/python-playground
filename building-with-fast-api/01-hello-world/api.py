from fastapi import FastAPI

app = FastAPI()


# Routes -----------------------------------------------------------------------
# The problem with using the `FastAPI()` instance is that it can only run ONE
# route, whereas the `APIRouter` class can allow multiple routes.

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello World" }
