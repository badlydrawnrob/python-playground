from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from database.connection import conn
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.events import event_router
import uvicorn

# ------------------------------------------------------------------------------
# A PLANNER app (SQLModel)
# ==============================================================================
# See earlier chapters for full instructions on FastApi etc. I like to treat some
# parts of the app as a "black box" (I don't need to know how it works, only that
# it works!), but it's best to get a senior (or book) to help you with this.
#
# 1. FastApi with models and routes (API layer)
# 2. PeeWee ORM (data layer) for CRUD operations
# 3. JWT tokens for authentication
#
# There's LOTS of things to learn, so it's easy to feel overwhelmed. I find it
# helpful to use a REPL to test out code snippets, and have a solid "learning
# frame", meaning knowing when to learn, and when to delegate. It's find to tell
# yourself "that's not for me, not my job". For me that's:
#
# 1. How to deploy a FastApi app to production (performance, DBA, etc)
#     - @ https://tinyurl.com/fastapi-preparing-production
# 2. Email verification and signup (with an SMS authenticator)
#     - This is non-trivial! I don't want to handle this.
# 3. Setting up JWT tokens, password hashing, and authentication
#    - All I want to know is how to write the `depends()` in the routes.
#
# ⚠️ Warnings
# -----------
# > FastApi is ASYNC, but PeeWee is NOT ...
# > See `database.connection` for more info.
# 
# See the following example on how to fix this (as well as the many Github issues
# on PeeWee repo (the alternative is
# `gevent` or queuing).
#    @ https://fastapi.xiniushu.com/uk/advanced/sql-databases-peewee
#
# The producer of PeeWee has this to say about async!
#    @ https://charlesleifer.com/blog/asyncio/
#
# > Changing ORMs and databases can be tricky!
# > Are your schema and models compatible?
#
# You need to make sure your schema and ORM are compatible! It might help to
# manually setup your schema and simply use the ORM for rows -> objects.
#
# > API layer and DATA layer splitting can be a little confusing.
# > Have a high-level view, somewhere so everything makes sense ...
# > Especially as you grow your team!
#
# For example, `Event.id` is handled by PeeWee, NOT Pydantic!
#
# > FastApi and SQLModel problems
#
# - We're now using PeeWee to handle our database layer
# - SQLModel joins I found to be far from intuitive, and the docs not great ...
# - @ https://tinyurl.com/sqlmodel-join-a-table-on (see commit `1.12.4` full notes)
#
#
# Notes
# -----
# > We're now separating our API and ORM models. Some say this is better.
# > If you tightly couple them, it's harder to switch to another ORM later!
#
# 1. For now, I handle migrations manually with raw SQL.
# 2. I try to be consistent with my function, and abstract where possible.
# 3. ORMs can create problems with your SQL statements (or schema) at scale.
#    - However you manage this, database rows need to be translated ...
#    - Meaning, row data needs to be converted to data models (or objects).
#    - If you choose to use raw SQL, be careful of malicious SQL injections.
# 4. `__init.py__` is a daft idea. It's a Python thing.
#    - @ https://stackoverflow.com/a/48804718
# 5. Decide if you need a `PUT` or `PATCH` request.
#    - Does your client send ALL the data or just some?
#
# I also don't like Python OOP style. Check out Elm Lang for typed functional
# style programming. Where possible, I'll use that style.
#
#
# Security
# --------
# > I'm not very confident with security, so I always have someone I trust check
# > over my code. It's important to protect yourself against hacks and keep your
# > API secure (things like email verification help).
#
# Things to consider:
# 
# 1. Malicious SQL injections and DDOS attacks.
# 2. Authentication and authorization (we use dependency injection).
# 3. Bearer tokens (JWT) for authentication. These are checked on each route.
#
#
# Wishlist
# --------
# > Remove code duplication. Simplify your code. If a thing can be removed,
# > remove it. Follow the "5 steps" that Tesla uses to build their cars.
#
# 1. Make sure all routes that require a logged in user are secured. Also check
#    that the "owner" of a data point is the only one who can edit/delete it.
#    - What can a non-owner do? What data points are private? (read, write, delete)
# 2. We can have a public ID (`UUID`) and a private (`Int ID`) one.
#    - FastApi automatically adds and increments an `id` on each table insert.
#    - We need a public facing ID for our `User` model (for our url)
#    - Our private ID is used for any database operations (`join`, `DELETE`, etc)
#    - We're currently using the user's email address as ID which isn't ideal.
# 3. Our `Event.creator` is the current users `ID`:
#    - As mentioned above, it's currently an email.
#    - Joins are quicker with an `Int ID` than a `String` (email)
# 4. Add a `private` option for our `Event` model (so only the user can see it)
# 5. ⭐ Our `User.events` relationship, which is now `JSON` data is used for a
#    `List ID` of events. However, it's FAR MORE COMPLICATED to use than when we
#    had a simple `List Int` when our `Event` was a `BaseModel` (not a SQLModel).
#    See the links below to see what I mean.
#    - ⭐ You have many routes for app architecture. Ask "why do I need this?"
#      and "how will it be used?". There's no real need for a `List Event.id` as
#      you can simply `join` on the events to the user! That's WAY EASIER!
#    - A `List Event.id` would be handy if it's a public API (like OpenLibrary),
#      where you'd want to `.andThen` to the Events API to get the events. But
#      that's not really needed for this app.
#     - To edit events we could have a `GET` request to `/user/{id}/events`
#       and a `POST` request to `/user/{id}/events/{event_id}` (or `DELETE`).
#     - @ https://stackoverflow.com/q/70567929 (using json columns)
#     - @ https://stackoverflow.com/q/79091886 (mutating a json column) but search
#       Brave with "Replacing JSON Column FastAPI" for better options.
#     - @ https://tinyurl.com/sqlite-peewee-and-json-data (it's even pretty
#       complicated with Peewee ORM)
# 6. Use abstraction to reduce code duplication.
# 7. Is the current encryption and hashing the most secure?
#    - Create a better `SECRET_KEY` perhaps.
# 8. Are results cached? (for performance, but add "just-in-time", not premature)
#    - @ https://github.com/long2ice/fastapi-cache
#    - @ https://www.powersync.com/blog/sqlite-optimizations-for-ultra-high-performance
# 9. Make `/signup` more graceful and user-friendly (or remove completely)
#    - Option 1: Have a simple "invite" process and manually create accounts
#    - Option 2: Find a professional and delegate the process
#        - Signup -> Email -> Verify (code) -> Login -> Onboarding
# 9. Remove all `/admin` routes, such as:
#    - `/event` (for deleting all events)
#    - These are dangerous and should never be allowed by anyone other than
#      admin (it's also highly unlikely it's needed!)
# 10. We could add `User.role` table, and add proper roles later:
#    - @ https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
# 11. Potentially use SQLite Utils to easily setup mock data
#    - We could have a development database that gets setup automatically
#    - And mock the live data with @ https://sqlite-utils.datasette.io/en/stable/
#    - How would we setup and teardown?
# 12. Understand type safety with Python a bit better:
#    - @ https://talks.jackleow.com/strongly-typed#slide-23
# 13. How are we creating the database?
#    - Consider leaving the `@app.on_event` decorator out of the code and doing
#      database setup manually.
#    - It's deprecated anyway, and now uses `lifespan` event handlers.
# 14. Understand "middleware" and when it's useful.
#    - @ https://fastapi.tiangolo.com/tutorial/middleware/
# 15. Tidy up the `dict` type in the function `return` values:
#    - Currently `pyright` complains that they aren't specific enough.
# 16. Create different `include_router` packages for authentication routes:
#    - @ https://fastapi.tiangolo.com/tutorial/bigger-applications/
#    - @ https://stackoverflow.com/a/67318405
# 17. Implement logging for FastApi live server and preparing for launch:
#    - @ Search Brave "fastapi logging production"
#    - @ https://tinyurl.com/prep-fastapi-for-production (hire a professional!)
# 18. We also need an "extend your session" route, which we can ping:
#    - If `< 15 minutes` then extend the session notification
# 19. Set SQLite to strict mode (and PRAGMA settings) on launch.
#    - I might remove the `conn()` function and setup the schema manually.
#    - The models are still handy, as this gives a high-level view of the schema.
# 20. Fix `.utcnow` to datetime (deprecated in `jwt_handler.py`)
# 21. Begin creating some simple tests for `join`s:
#    - Task 1: Get the specific user events where user.email == events.creator
#    - Task 2: Get the full `User` and `join` on the `Event` table
#    - @ https://stackoverflow.com/questions/21975920/peewee-model-to-json
#    - @ https://sqlmodel.tiangolo.com/tutorial/connect/read-connected-data/
#    - @ https://docs.peewee-orm.com/en/latest/peewee/querying.html
# 22. Some way to manage our data points from a high-level view
#    - For example, which FastApi fields are `Optional()`?
#    - Which are automatically handled (or handled) by PeeWee?

app = FastAPI()

# Register our routers ---------------------------------------------------------
# Prefix the `/user`: `/user/signup` and `/user/signin` (same for event)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# Middleware -------------------------------------------------------------------
# A list of allowed CORS origins (by default only the same domain)
# @ https://fastapi.tiangolo.com/tutorial/cors/ (wildcard, or list of domains)

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database build ---------------------------------------------------------------
#! Is there a way to automatically build our database schema with PeeWee?

@app.on_event("startup")
def on_startup():
    pass

# Routes -----------------------------------------------------------------------
    
@app.get("/")
def home():
    return RedirectResponse(url="/event/")

# Run our app ------------------------------------------------------------------
# This is slightly different from the book code, which errors (see chapter_07)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
