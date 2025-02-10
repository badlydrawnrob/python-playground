from fastapi import FastAPI

from database.connection import conn
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.events import event_router
import uvicorn

# ------------------------------------------------------------------------------
# A PLANNER app
# ==============================================================================
# See earlier chapters for full instructions on FastApi etc. Now we have our app
# architecture sorted, it's time to set up an ORM, our SQL database, and allow
# CRUD (create, read, update, delete) operations with SQLModel (or MongoDB in
# the book)
#
# Notes
# -----
# We're using SQLModel, which is from the same creator of FastApi, and will allow
# us to use our Pydantic models as a basis for our SQL tables. WARNING: This has
# been said to not be the best setup, as it tightly couples your SQL models from
# your API design. Many say it's better to keep these two separate.
# 
# Currently this doesn't specifiy that ONLY signed in users can create and update
# events, as there's no auth involved. We'll need to add those checks in.
#
# Questions
# ---------
# 1. How does the `create_engine()` method work?
#    - `echo=True` prints out the SQL commands carried out
# 2. Do we only need to setup database ONCE?
#    - `.create_all(engine)` is an instance of `create_engine()`
#    - This creates the database and the tables we've defined in model
# 3. What does `RedirectResponse()` mean, or do?

app = FastAPI()

# Register our routers ---------------------------------------------------------
# We're prefixing the `/user`: `/user/signup` and `/user/signin`

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# Database stuff ---------------------------------------------------------------
# These will help initiate our database.
#
# Notes
# -----
# `@app.on_event` is deprecated. Use `lifespan` event handlers instead.
#    @ #! https://fastapi.tiangolo.com/advanced/events/

@app.on_event("startup") #!
def on_startup():
    conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

# Run our app ------------------------------------------------------------------
# If you try running this as `.run(app, ...)` you'll get an error:
#   "pass the application as an import string to enable 'reload' or 'workers'"
# The book also uses `0.0.0.0` as the host, but `localhost` is more secure.

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
