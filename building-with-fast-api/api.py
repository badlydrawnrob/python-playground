from fastapi import FastAPI

app = FastAPI()


# Routes -----------------------------------------------------------------------

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello World" }
