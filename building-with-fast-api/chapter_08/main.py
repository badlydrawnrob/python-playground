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
# See earlier chapters for full instructions on FastApi etc. We have models,
# an ORM for SQLite, and performing CRUD operations on our routes. Some of those
# routes are protected by authentication, for which we use JWT tokens that get
# passed to our routes with a Bearer token header (after login). Some parts of
# the app can now be viewed as a "black box", where we only need surface-level
# knowledge of what it does (not how, we hire a professional for that).
#
# There really is a LOT to learn with FastApi, http servers, REST APIs, and SQL.
# If you're feeling overwhelmed, better to find a good mentor! As always, it's a
# good idea to develop a "learning frame" to know when to say "cool, I'll learn
# that", and when to say "that's not my job" and skip/delegate it.
#
# For example, "that's not my job" could be:
#
# - How to deploy a FastApi app to production (performance, DBA, etc)
# - Email verification and signup (with an SMS authenticator)
# - Settings up JWT tokens and authentication routes
#
# Notes
# -----
# > Some say you should separate your API and ORM models.
# > Tightly coupling them means it's harder to switch to another ORM.
#
# 1. Each ORM does things a bit differently, so try to separate concerns where
#    possible. For example, migrations could be handled manually (rather than
#    using Alembic)
# 2. Try to be consistent: for example, I'm using slightly different `.select()`
#    methods in each function. Abstract your functions and simplify.
# 3. ORMs can create problems with your SQL statements (or schema) at scale. Keep
#    things simple for now with SQLModel. Consider other options later:
#    - You'll need to translate database rows to data models whatever you choose,
#      and this is tricker to do when working with raw SQL rows. Use `SQLAlchemy
#      text` or `sqlite3` directly, but protect agains malicious SQL injections.
#    - Lightweight query packages like PyPika and Pony ORM are also worth a look.
#    - @ https://tinyurl.com/object-relational-mapping-sql (nice article)
# 4. `__init.py__` is a dumb idea (it's a Python thing). Indicates a package dir.
#    - @ https://stackoverflow.com/a/48804718
#
# Security
# --------
# > If you're not comfortable dealing with security (like me) hire a professional
# > to double check your code, or prevent hacks for you. There's many other
# > ways to keep your API secure (such as email verification).
#
# 1. Protect yourself from malicious SQL injections
# 2. Dependency Injection is a design pattern to force a function to run before
#    performing the main body of the function. Auth is a good example of this.
#    FastApi can use a function or a class for this.
# 3. Bearer tokens (JWT) are a way to authenticate users. Use `Dependency()` to 
#    force authenticated user login (on routes) before the function can run.
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

@app.on_event("startup")
def on_startup():
    conn()

# Routes -----------------------------------------------------------------------
    
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

# Run our app ------------------------------------------------------------------
# This is slightly different from the book code, which errors (see chapter_07)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
