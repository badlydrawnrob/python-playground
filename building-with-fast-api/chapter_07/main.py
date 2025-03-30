from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
# Security
# --------
# > Dependency Injection is a pattern where an object (in our case a function)
# > receives an instance variable needed for further execution of the function.
# > In FastApi a dependency can be defined as either a function or a class.
# 
# In FastApi a bearer token (JWT) is an authentication method that is
# injected into FastApi as dependencies called at runtime. They are dormant
# until injected into their place of use. There's many other ways to keep your
# API secure and it's worthwhile hiring a security expert.
#
# Wishlist
# --------
# 1. We want to assure that the right logged in user edits their (and only their)
#    events. They shouldn't be able to see or work with other people's events.
# 2. We should have a `UUID` and a `ID` which is unique for each user.
#    - The `UUID` is public and the `ID` is private
#    - The `UUID` is used instead of the user's email address (in authenticate)
# 3. Our `Event` model should have a `User` field (for ownership)
#    - It may be a dumb idea to have a `User.events` list (as there could be many)
#    - If you need `json` list of events, you could use a `User.events` method
# 4. Reduce code duplication (for example, similar `SELECT` statements)
#    - Abstract this into a function (or a class)
# 5. Check which encryption and hashing is most secure (or secure enough)
#    - For instance, create a better `SECRET_KEY` perhaps.
# 6. A `private` option for our `Event` model (so only the user can see it)
# 7. Are results cached? (for performance)
#    - @ https://github.com/long2ice/fastapi-cache
#    - @ https://www.powersync.com/blog/sqlite-optimizations-for-ultra-high-performance
# 8. Remove all `/admin` routes, such as:
#    - `/admin/events` (for deleting all events)
#
# Questions
# ---------
# 1. `@app.on_event` creates database if doesn't exist
#    - This can safely be left out if you're manually creating your database
#    - #! Deprecated: use `lifespan` event handlers instead
# 2. What the fuck is `__init__.py`? It makes no sense to me.
#    - @ https://stackoverflow.com/a/448279 (regular and namespaced packages)
#    - @ https://stackoverflow.com/a/48804718
# 3. What's the best and most user-friendly way to authenticate users?
#    - #! This isn't something I feel comfortable setting up myself!
# 4. What the fuck does "Middleware" mean?

app = FastAPI()

# Register our routers ---------------------------------------------------------
# We're prefixing the `/user`: `/user/signup` and `/user/signin`

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# Middleware -------------------------------------------------------------------
# A list of allowed CORS origins (by default only the same domain)
# @ https://fastapi.tiangolo.com/tutorial/cors/

origins = [
    "http://localhost:8000" # a list of domains, or `"*"` wildcard for any origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
