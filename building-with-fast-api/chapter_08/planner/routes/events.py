# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Our app routes use Pydantic for API data validation and Piccolo ORM for our
# data models. SQLite is not strict by default, so we've got to be extra careful.
# If there's sensitive information we don't wish to expose, we can use the
# `response_model=` with the correct Pydantic model.
#
#
# Coding style
# ------------
# > Same name, but `tables.Event` and `models.Event` are different!
# > Namespaces look kind of fugly, but I'll keep them in to be clear.
#
# We're namespacing our modules to make it clear whis is API and Data. You may
# find this version difficult to read and prefer to be explicit with your models,
# such as `EventData` and `EventAPI` or similar. Modules should be lowercase in
# Python PEP8 styleguide (unlike Elm).
#
#
# Async only
# ----------
# > ⚠️ Avoid endpoints that contain both read and write functions!
# > See the `planner.tables` file for more information on `IMMEDIATE` transactions.
#
# Unfortunately we've got to pepper our code with `async` and `await` keywords.
#
# It's easier to have atomic update/insert/delete queries. Make sure you have all
# the data you need to perform the WRITE (such as a `BaseUser.Id` with the `authenticate()`
# function); this way you can avoid also having to READ (`Event.creator` would
# otherwise need a `BaseUser.select`). Otherwise you're going to run into the
# problem with read and writes, leading to "database locked" errors. Peewee also
# had this problem. Postgres doesn't have this problem.
#
#
# Data validation
# ---------------
# > We're not running SQLite in strict mode!
# > Postgres doesn't have this problem (it's always strict).
# > Pyright complains if you return vague `dict` types!
# 
# Which means SQLite will accept whatever you give it by default ... ANY data.
# Any data at all. We could set `STRICT TABLES` but that'd limit our Piccolo
# column types, so instead be sure to validate with Pydantic _before_ inserting
# data into a row.
#
#
# User experience
# ---------------
# 1. `DELETE` data should always prompt the user to confirm
# 2. Your privacy policy should be honoured: don't leak sensitive information!
# 3. Non-public-facing urls should be heavily secure or localhost-only
#
#
# FastApi functions
# -----------------
# > I generally prefer Elm-style, whereby you'd avoid "magic" and convert the
# > data directly to whatever form (types) you needed. Pydantic response types
# > do saves us time and are quite graceful.
#
# 1. Response types come in two flavours:
#     - `-> Response` -or- `response_model=`
#     - You generally do not want (or need) to use both!
# 2. `Depends(authenticate)` runs before the route function
#     - It fails if user is not logged in
#
#
# Questions
# ---------
# 1. #! How best to check for `None` or `[]`?
#     - Write a very short article on this?
#     - `RETURNING` -vs- `SELECT` guards (opt for the former generally)
# 2. Positive or negative guards?
# 3. Do I understand what `Depends()` is doing? (visualise)
# 4. Do I understand what path, query, and request parameters are?
# 5. Do I understand what named keyword arguments are? (plus `**kwargs`)
#
#
# WISHLIST
# --------
# > Make sure routes are properly secured
#
# 1. Write an article about making `/signup` more graceful with Piccolo, and how
#    each option affects usability and experience (Artifacts):
#    - Option 1: Have a simple "invite" process and manually create accounts
#    - Option 2: Find a professional and delegate the process
#        - Just how much would this cost? (via Ai / via Human)
#        - Signup -> Email -> Verify (code) -> Login -> Onboarding
# 2. Create different `include_router` packages for authentication routes?
#    - @ https://fastapi.tiangolo.com/tutorial/bigger-applications/
#    - @ https://stackoverflow.com/a/67318405

from auth.authenticate import authenticate
from fastapi import APIRouter, Depends, HTTPException

from piccolo.apps.user.tables import BaseUser
from piccolo.engine.sqlite import TransactionType #! ⚠️ Try to avoid using this!

import planner.tables as data # data.Event
import planner.models.events as api # api.Event

from typing import List


event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# ------------------------------------------------------------------------------
# Read routes
# ==============================================================================

@event_router.get("/", response_model=List[api.Event])
async def retrieve_all_events() -> List[api.Event]:
    """Return a simple list of events!
    
    You could use Piccolo's `create_pydantic_model` to generate our response
    types, but we're being explicit in `planner.models.events`. You could also
    return a particular data point explicitly if you prefer:

    ```
    [{"title": event.title} for event in query]
    ```
    """
    query = await data.Event.select()

    return query


@event_router.get("/{id}")
async def retrieve_event(id: str) -> api.Event:
    """Retrieve a single event by UUID
    
    > ✅ Piccolo is a lot more terse and pleasant than Peewee in some ways.
    
    Any exceptions are dealt with by `HTTPException`. There are other ways we
    could raise errors, such as `RecordNotFound`. I dislike  `try/except/finally`
    blocks, so avoiding them like the plague!
    """
    event = await data.Event.select().where(data.Event.id == id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail=f"Event with ID: {id} does not exist"
        )
    
    return event


# ------------------------------------------------------------------------------
# Write routes
# ==============================================================================

@event_router.post("/new")
async def create_event(
    body: api.Event,
    user: int = Depends(authenticate)) -> api.Event:
    """Create a new event

    > ✅ `Event.id` is auto-generated by Piccolo.
    > ✅ `authenticate() -> username | error` (no need to check again)

    1. Our user `id` is required to create the event.
    2. Our event has a `UUID` which can be shortened for prettier URLs.

    We've avoided having an `IMMEDIATE` transaction here, as our authenticate
    function now returns the user `ID` which we can use for `creator=`.

    Security
    --------
    - ⚠️ Never expose sensitive information like `ID` in responses (security)

    Errors
    ------
    > Possible things that can go wrong ...

    - We do not use guards to check if an event exists (use SQLite errors)    
    """
    event = body.model_dump(exclude_none=True) # Event -> dict

    query = await (
        data.Event.insert(
            data.Event(creator=user,**event)
        )
        .returning(*data.Event.all_columns()) # Return full record
    )

    return query[0] #! Is there a more graceful way to do this?


# ------------------------------------------------------------------------------
# Delete routes (destructive actions)
# ==============================================================================
# > ⚠️ `DELETE` all route has been removed for safety (just admin raw SQL)
#
# Be super careful with any `DELETE` routes! You should always notify the user
# and have them confirm the action. In production you may wish to avoid certain
# `DELETE` routes altogether (like deleting all events).

@event_router.delete("/{id}")
async def delete_event(id: str, user: int = Depends(authenticate)) -> dict:
    """Delete an event by ID

    Errors
    ------
    > Possible things that can go wrong ...

    1. ⚠️ User who doesn't own data tried to delete it
    2. 🔐 "Database locked" error with SQLite async (now not possible)
    3. ...
    """
    query = await (
        data.Event.delete()
        .where(
            (data.Event.id == id) & (data.Event.creator == user)
        )
        .returning(data.Event.id) #! Use this instead of `id`?
    )

    if not query: # Is an empty list?
        raise HTTPException(
            status_code=404,
            detail=f"Event with supplied ID: {id} does not exist"
        )

    return { "message": f"Event with ID# {id} deleted!" }


# ------------------------------------------------------------------------------
# Deprecated routes (old SQLModel code for reference)
# ==============================================================================
# I've left in the old `PATCH` update route with `SQLModel` for reference, but
# I feel it's safer to use `PUT` to replace the entire resource. (Be explicit!)


# @event_router.patch("/edit/{id}", response_model=Event)
# def update_event(id: int, data: EventUpdate, user: str = Depends(authenticate)) -> Event:
#     event = session.get(Event, id) # Get `Event` object from database

#     if not event: # is `None` if event doesn't exist
#         raise HTTPException(status_code=404, detail="Event not found!")
    
#     #! Positively check or negatively check? (preference)
#     if event.creator != user: # Check if user is creator of event
#         raise HTTPException(
#             status_code=400,
#             detail="You can only update events that you've created"
#         )

#     event_data = data.model_dump(exclude_unset=True) # EventUpdate(BaseModel) could be used instead
#     event.sqlmodel_update(event_data) # Update new `Event` object (see Q11)
#     session.add(event)
#     session.commit()
#     session.refresh(event)

#     return event # If you don't return something you'll get `Internal Server Error`!
