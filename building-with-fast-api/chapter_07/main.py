from fastapi import FastAPI

from database.connection import conn
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.events import event_router
import uvicorn

# ------------------------------------------------------------------------------
# A PLANNER app (SQLModel)
# ==============================================================================
# See earlier chapters for full instructions on FastApi etc. We've got our app
# architecture: our Models, ORM, SQLite database, and performing CRUD operations
# on our data. You might find that backend development is a bit more complicated
# than frontend ... as there's a lot more to consider.
#
# Notes
# -----
# > 💡 I'm testing out different `.select()` methods in this repo!
#
# There's a bunch of ways to write SQL queries, such as:
# 
# 1. SQLModel and other ORMs, such as Peewee
# 2. Query builders like PyPika (or roll your own):
#    - @ https://death.andgravity.com/own-query-builder is also interesting
# 3. Writing raw SQL queries:
#    - Such as SQLAlchemy text, or using `sqlite3` directly
#    - You've got to manually protect against malicious SQL injections
#
# For options (1) and (2) you'd need map your database rows to your Pydantic models,
# or whatever data structures you're working with: @ https://tinyurl.com/object-relational-mapping-sql
#  
# > Some say that you should separate your API and ORM models.
# > They say they shouldn't be tightly coupled (as SQLModel does).
#
# 1. SQLModel allows us to use Pydantic with FastApi (managing types)
#    - It uses SQLAlchemy under the hood
# 2. Peewee is another alternative, but requires running in parallel ...
#    - So you won't be able to reuse your Pydantic models
#
# Wishlist
# --------
# 1. We only want to allow logged in `User`s to create and update events
# 2. Our `Event` model should have a `User` field (for ownership)
# 3. For that to happen we need an auth system, with a JWT token (or similar)
# 4. Reduce code duplication (for example, similar `SELECT` statements)
#    - Abstract this into a function (or a class)
#
# Questions
# ---------
# 1. `@app.on_event` creates database if doesn't exist
#    - This can safely be left out if you're manually creating your database
#    - #! Deprecated: use `lifespan` event handlers instead
# 2. What the fuck is `__init__.py`? It makes no sense to me.
#    - @ https://stackoverflow.com/a/448279 (regular and namespaced packages)
#    - @ https://stackoverflow.com/a/48804718

app = FastAPI()

# Register our routers ---------------------------------------------------------
# We're prefixing the `/user`: `/user/signup` and `/user/signin`

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# Database build ---------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    conn()

# Routes -----------------------------------------------------------------------
    
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

# Run our app ------------------------------------------------------------------
# This is `.run(app, host="0.0.0.0")` in the book, but errors:
#   "pass the application as an import string to enable 'reload' or 'workers'"

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
