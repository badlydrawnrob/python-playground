# ------------------------------------------------------------------------------
# A PLANNER app (SQLModel)
# ==============================================================================
# > We're now using Piccolo ORM instead of SQLModel. The book uses MongoDB for
# > Chapters 6—8; after three attempts with different ORMs I've settled on Piccolo.
#
# This is for a few reasons:
#
# 1. Piccolo is ASYNC, so works well with FastApi (unlike PeeWee).
#     - Notes on async: @ https://github.com/piccolo-orm/piccolo/issues/1319
# 2. Piccolo has better documentation for querying the database.
#     - A nice playground feature: @ https://tinyurl.com/piccolo-playground-docs
# 3. Piccolo feels a bit lighter to use than the other ORMs I tried.
#     - Users are built-in: @ https://tinyurl.com/piccolo-user-creation
# 4. Piccolo doesn't require `open()`ing and `closing()` the database.
#     - It handles connections for you (unlike PeeWee).
# 5. Piccolo is relatively boring and stable (that's a good thing!)
#
# Versions
# --------
# > 1. I found SQLModel docs verbose and hard to work with.
# > 2. PeeWee used objects quite heavily and SQLite async buggy ...
# 
#     @ https://github.com/badlydrawnrob/python-playground/releases/tag/1.12.4
#     @ https://github.com/badlydrawnrob/python-playground/releases/tag/1.12.11
#
#
# Coding style
# ------------
# > Prefer functional programming over OOP where possible.
# > Have a clear goal and learning frame to operate within.
# 
# 1. Use as little code as possible to achieve the goal.
# 2. Never use objects where a function will do!
# 3. Always validate types and data with Pydantic.
# 4. There's too much to learn, so cherry pick.
# 5. Never prematurely optimise (fix just-in-time).
# 6. There's a lot could go wrong (fix just-in-time).
# 7. Prefer explicit code over implicit code (`PUT` > `PATCH`).
# 8. Ignore the hard bits (delegate, or learn later).
# 9. Never satisfice. Cross out all the wrong (or complex) routes.
#
#
# The hard bits
# -------------
# > Things I've decided I'm not prepared to learn, or do:
#
#     - Email notification and verification
#     - JWT verification and validation (mostly rely on the book)
#     - Migrations (use `sqlite-utils` or manual SQL for now)
#     - Server management and deployment
#     - Writing unit tests (test manually for now)
#
# Authentication and authorization are handles using dependency injection.
# Bearer tokens (JWT) for authentication. These are checked on each route.
# 
#
# Architecture
# ------------
# > Some areas I like to treat as a "black box" whereby I set it and forget it.
# > For prototyping, vibe coding, jobbing devs: you don't need to know everything!
#
# 1. FastAPI (API layer)
# 2. Pydantic models (API data validation layer)
# 3. Piccolo ORM models (data layer)
# 4. Piccolo ORM database (SQLite)
# 5. JWT tokens (authentication layer)
#
# It seems best to split the models into API and Data layers. This way you can
# switch out the ORM or API framework more easily later on. Some routes should
# be protected in a real-world app, so users don't see protected data.
#
#
# SQLite
# ------
# > There's downsides and upsides to SQLite
#
# 1. It's great because it's easy to backup and move around (just a file)
# 2. It's rubbish because it's not strict by default (like Postgres)
#     - So for type safety you always validate with Pydantic models first.
# 3. It does not have to deal with sessions (unlike client-server DBs)
#
#
# The downsides of FastApi and ORMs
# ---------------------------------
# FastApi:
# > There's better languages for web APIs, but unless they're 10x faster, productive,
# > or enjoyable to use, it's not really worth switching.
#
# I think the whole concept of async in Python is a bit dumb. At least the way it
# scatters your code with `await` and `async` keywords. The producer of PeeWee has
# this to say about async:
#
#    @ https://charlesleifer.com/blog/asyncio/
#
# ORMs:
# > ORMs can create problems with your SQL statements (or schema) at scale.
# > Our rule is "never prematurely optimise", so we'll worry about that later.
#
# Without an ORM you'd have to manually manipulate your database rows, converting
# them to the dictionaries FastApi expects. You'll likely get a boost in performance
# by writing SQL directly (you can do so with Piccolo), but you must be VERY
# careful of malicious SQL injections.
#
#
# WISHLIST
# --------
# > Remove code duplication and keep code simple (your future stupid self!)
#
# 1. ✂️ Go through the "5 steps" Tesla uses to build their cars.
#     - @ https://tinyurl.com/tesla-5-steps
# 2. 🔐 Make sure all routes that require a logged in user are secured.
#     - ⭐️ Understand `aud`ience and `client_id` in auth better:
#       @ https://stackoverflow.com/a/28503265
#     - Users can only view their own events for `/user/me` endpoint:
#       `user.email == events.creator` guards (or `WHERE`)
#     - Any actions on an event (like, delete) should check user "owns" it.
#     - Any unecessary destructive routes should be removed (will it torpedo the app?)
# 3. Can we tighten up security any more? (low hanging fruit)
#     - XSS attacks and SQL injections
#     - Error messages that give away too much info
#     - Destructive endpoints that aren't necessary
# 4. ⚠️ Are our TYPES strong enough? (we've only got API layer models)
#     - `int` is probably fine for `BaseUser.id`
#     - 💾 Try to insert bad data (does SQLite allow it?)
#     - 💾 Does SQLite always error on unique constraints? Any holes?
#     - Is there any need for `DataIn` types to verify insert/update?
# 5. ⚠️ Handling errors better (and some light unit testing)
#     - See "APIs you won't hate 2" book for error codes (out of scope). FastAPI
#       doesn't make it particularly easy to use best practice return values.
#     - In Elm you can `case` over errors more easily than Python.
#     - 🐛 What obvious errors are we not currently handling?
#         - ⚠️ Are all error codes correct (status, return values, etc)
#         - Low hanging fruit? What's YAGNI and just-in-time handling?
#     - What's the correct response and error codes per route?
#         - Are `HTTPExceptions` enough? What error codes should we use?
#         - Must you use `try/except` blocks in certain cases?
#         - Must you use particular error types? (`RecordNotFound`, etc)
#         - 💾 SQLite integrity, null constraint, duplicate value errors?
#         - 💾 Write AT LEAST a duplicate ID function (SQLite unique constraint)
#     - Any `DELETE` operations need careful error handling"
#         - 🔐 Are all routes secured properly?
#         - 👩‍🦳 Can a user who doesn't own a piece of data delete it?
#         - ⚠️ Sensitive data we should never return (the `ID` or "BE VAGUE")
# 6. Consider using some GUI to aid "birds eye view" of schema/data
#     - I think Piccolo has some rudimentary version of this, and Admin
#     - See "APIs you won't hate" for more ideas (error codes, etc)
# 7. Consider shortening the `UUID` type for prettier URLs.
#     - This can be done after the fact (`UUID` -> `ShortUUID`)
#     - @ https://github.com/piccolo-orm/piccolo/issues/1271
#     - #! Order of speed for lookup/joins: `Int` > `Bytes` > `String`
# 8. ⏰ Bombardier test for concurrency and speed
#     - Remember 100s of connections may be unlikely; prefer solid to speedy
#     - ⚠️ Any `POST` endpoints require getting the `BaseUser.id` first.
# 9. SQLite pragma optimizations for performance
#     - Things like `-wal` and `-shm` modes
#     - @ https://github.com/piccolo-orm/piccolo/discussions/1247
# 10. Write down the reason to prefer `PUT` over `PATCH`
#     - Patch is harder to predict which optional values are present
#     - Similar to the Elm `Decode.maybe` problem
#     - @ https://sqlmodel.tianglo.com/tutorial/fastapi/update
# 11. ⚠️ `List Int` for tags is far more complicated than simple join
#     - Would this be a many-to-many relationship?
#     - What difference does this make to UI and architecture?
#     - Does it make the Elm Lang code easier or harder?
#     - How are others handling this and their endpoints?
# 12. Do we need any caching? (on the server or with SQlite)
#     - @ https://github.com/long2ice/fastapi-cache
#     - @ https://www.powersync.com/blog/sqlite-optimizations-for-ultra-high-performance
# 13. `BaseUser` could contain a `UUID` and `User.role`?
#     - A `UUID` might be hard to retrofit on the main user table
#     - @ https://tinyurl.com/piccolo-extending-base-user
#     - @ https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
# 14. Understand middleware a little better
#     - @ https://fastapi.tiangolo.com/tutorial/middleware/
# 15. Logging for FastApi live server to prepare for launch:
#     - @ Search Brave "fastapi logging production"
#     - @ https://tinyurl.com/prep-fastapi-for-production (hire a professional!)
# 16. Disallow some email addresses if we're not in control of signup
#     - For example `user+test@gmail` which allows multiple accounts.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from piccolo.table import create_db_tables

from planner.routes.users import user_router
from planner.routes.events import event_router
from planner.tables import Event

import uvicorn


# ------------------------------------------------------------------------------
# Create the app instance
# ==============================================================================
# > See also my `data-playground/mocking/fruits` repo for further explanations
#
# 1. Build the database (if doesn't already exist)
# 2. Use the `lifespan` setup
# 3. Set a simple home route

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables(Event, if_not_exists=True)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return RedirectResponse(url="/event/")


# ------------------------------------------------------------------------------
# Routers (register)
# ==============================================================================

app.include_router(user_router, prefix="/user") # prefixes the `/user` url
app.include_router(event_router, prefix="/event") # prefixes the `/event` url


# ------------------------------------------------------------------------------
# Middleware
# ==============================================================================
# Tightens up security: @ https://fastapi.tiangolo.com/tutorial/cors/

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


# ------------------------------------------------------------------------------
# Run app
# ==============================================================================
# Slightly different from the book code which errors (see chapter_07)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
