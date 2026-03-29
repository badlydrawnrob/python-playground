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
# 1. Always validate types and data with Pydantic.
# 2. Brutalist, minimalist, zen (`Task._meta.primary_key` -> `Task.id`)
# 3. Ignore the hard bits (delegate, or learn later).
# 4. Never prematurely optimise (fix just-in-time).
# 5. Never use objects where a function will do!.
# 6. Never satisfice. Cross out all the wrong (or complex) routes.
# 7. Objects only ever to be used if dramatically enhances performance
# 7. Prefer explicit code over implicit code (`PUT` > `PATCH`).
# 8. There's a lot could go wrong (fix just-in-time).
# 9. There's too much to learn, so cherry pick.
# 10. Use as little code as possible to achieve the goal.
# 11. Work directly with data (rather than classes and methods)
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
# Downsides of FastApi and ORMs
# -----------------------------
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
#     - ⚠️ `List Int` tags far more complicated than simple join (many-to-many?)
#     - How is UI architecture affected by endpoint design? (easier/harder?)
#     - How are others handling this and their endpoints?
#     - Elm code be made easier? (e.g: don't check UNIQUE values on client)
# 2. Use Serial `ID` and shorter `UUID` for prettier URLs (and speed)
#     - Likely faster to have Serial `ID` for internal lookups
#     - You could convert `UUID` to `ShortUUID` on the frontend, but a short
#       uuid may also be quicker for lookups.
#     - @ https://github.com/piccolo-orm/piccolo/issues/1271
# 3. ⚠️ Are our TYPES strong enough? (we've only got API layer models)
#     - `int` is probably fine for `BaseUser.id`
#     - 💾 Try to insert bad data (does SQLite allow it?)
#     - 💾 Does SQLite always error on unique constraints? Any holes?
#     - Is there any need for `DataIn` types to verify insert/update?
# 4. ❌ Essential errors should be handled somewhere (but don't prematurely optimise)
#     - Response codes, error messages, status codes, etc.
#     - ❌ `try`/`except` doesn't work for `sqlite3.OperationalError: database is locked`
#       etc, so will need to be handled by the client or fixed somehow.
# 5. 🔍 Logging for FastApi live server to prepare for launch:
#     - @ Search Brave "fastapi logging production"
#     - @ https://betterstack.com/community/guides/logging/logging-with-fastapi/
#     - @ https://tinyurl.com/prep-fastapi-for-production (hire a professional!)
# 6. Can we tighten up security any more? (low hanging fruit)
#     - XSS attacks and SQL injections
#     - Error messages that give away too much info
#     - Destructive endpoints that aren't necessary
# 7. Create different `include_router` packages for authentication routes?
#    - @ https://fastapi.tiangolo.com/tutorial/bigger-applications/
#    - @ https://stackoverflow.com/a/67318405
# 8. Consider using some GUI to aid "birds eye view" of schema/data
#     - I think Piccolo has some rudimentary version of this, and Admin
#     - See "APIs you won't hate" for more ideas (error codes, etc)
# 9. `BaseUser` could contain a `UUID` and `User.role`?
#     - @ https://tinyurl.com/piccolo-extending-base-user
#     - @ https://fastapi.tiangolo.com/advanced/security/oauth2-scopes
#     - This might be hard to retrofit and may require custom user table
# 10. Understand middleware a little better
#     - @ https://fastapi.tiangolo.com/tutorial/middleware/
# 11. Disallow some email addresses if we're not in control of signup
#     - For example `user+test@gmail` which allows multiple accounts.
# 12. ⏰ Do we need any other speed optimisations like caching?
#     - @ https://github.com/long2ice/fastapi-cache
#     - @ https://www.powersync.com/blog/sqlite-optimizations-for-ultra-high-performance

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from piccolo.table import create_db_tables

from planner.routes.users import user_router
from planner.routes.events import event_router
from planner.tables import Event

import time #! See `README.md#-performance`

import uvicorn


# ------------------------------------------------------------------------------
# Create the app instance
# ==============================================================================
# > See also my `data-playground/mocking/fruits` repo for further explanations
#
# 1. Build the database (if doesn't already exist)
# 2. Use the `lifespan` setup
# 3. Set a simple home route
#
# We could've also used Piccolo Admin here:
#
# ```
# admin = create_admin(tables=APP_CONFIG.table_classes)
# app.mount("/admin", admin)
# ```

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables(Event, if_not_exists=True)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return RedirectResponse(url="/events/")


# ------------------------------------------------------------------------------
# Routers (register)
# ==============================================================================
# > Use plural nouns for collections and singluar for single resources.

app.include_router(user_router, prefix="/users") # prefixes the `/users` url
app.include_router(event_router, prefix="/events") # prefixes the `/events` url


# ------------------------------------------------------------------------------
# Middleware
# ==============================================================================
# Tightens up security: @ https://fastapi.tiangolo.com/tutorial/cors/
#
# 1. ⚠️ Can slow performance! Not essential but very handy for client. Changed
#    header from `X-Process-Time` to `Server-Timing` to follow best practice,
#    where you could communicate one or more performance metrics.
#    - @ https://fastapi.tiangolo.com/tutorial/middleware/#create-a-middleware
#    - @ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Server-Timing
#    - ⚠️ See `README.md#-performance` for a better way!

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["Server-Timing"] = f"app;dur={process_time}" # {process_time * 1000:.2f}
    return response


# ------------------------------------------------------------------------------
# Run app
# ==============================================================================
# > The timeout is not strictly necessary but it's the same as `SQLiteEngine().
# > See `../../PERFORMANCE.md` for more on this.
#
# Slightly different from the book code which errors (see chapter_07)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, timeout_keep_alive=10)
