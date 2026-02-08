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
# > ⚠️ SQLite is NOT in strict mode. We only have API layer models.
# 
# SQLite will validate `null` and `unique` constraints. We are not currently
# validating our `DataIn` types; SQLite is lax at typing, and we are NOT operating
# in strict mode! You may also wish to add a DATA layer for more concrete validation,
# so that we can assure correct types on insert and update.
#
# This means SQLite will potentially accept whatever you throw at it ... ANY data.
# We could set `STRICT TABLES` but that'd limit our Piccolo column types. For
# now we're leaning on the API layer to validate things. Postgres doesn't have
# this problem (it's always strict).
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
# 1. ⏰ Are there any design routes that are QUICKER?
#    - E.g: using `match` and `case` (or some other method)
# 2. ✏️ Write an article about making `/signup` more graceful with Piccolo, and how
#    each option affects usability and experience (Artifacts):
#    - Option 1: Have a simple "invite" process and manually create accounts
#    - Option 2: Find a professional and delegate the process
#        - Just how much would this cost? (via Ai / via Human)
#        - Signup -> Email -> Verify (code) -> Login -> Onboarding

from auth.authenticate import authenticate
from fastapi import APIRouter, Depends, HTTPException, Query

import planner.tables as data # data.Event
import planner.models.events as api # api.Event

from typing import Annotated, List


event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# ------------------------------------------------------------------------------
# Read routes
# ==============================================================================

@event_router.get("/", response_model=List[api.Event])
async def retrieve_all_events(
        q: Annotated[str | None, Query(min_length=4, max_length=8)] = None
    ) -> List[api.Event]:
    """Return a queryable list of events!

    > Default order is by primary key INDEXED number, which means the `Event.id`
    > will appear in the order it was inserted (not by ABC123 order).
    
    Out API layer models are custom and we can use them as response types. You
    could also return particular data points explicitly if you prefered:

    ```
    [{"title": event.title} for event in query]
    ```

    Queries (list by column)
    ------------------------
    > We'll replicate a table sort by column (ASCENDING by only)

    1. By title
    2. By location

    Annotated
    ---------
    > @ https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

    `Annotated` is used so that we can keep our typing `str | None = None`,
    otherwise the typing would need a workaround. We can add metadata such as
    `deprecated=True`, `pattern="RegEx"`, and further validation methods to check
    our `?q`uery keys and arguments. FastAPI will automatically add relevant `/docs`
    information.

    Errors
    ------
    > Be careful of your endpoint url structure

    1. ✅ `event/?q=title` (feels wrong but is right)
    2. ❌ `event?q=title` (feels right but is wrong)
    """
    query = data.Event.select()

    if q == "title":
        return await query.order_by(data.Event.title)
    elif q == "location":
        return await query.order_by(data.Event.location)
    else:
        return await query


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

    1. ❌ User enters text that isn't a plain string (strip HTML before insert)
    2. ❌ Event already exists (we're not properly checking duplicate values)
    3. ❌ Event should not pass validation if `exclude_none=False` (see Bruno)
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

    1. <s>🔐 "Database locked" error with SQLite async<s> (no read then writes)
    2. <s>⚠️ User who doesn't own data tried to delete it</s> (we've handled this)
    3. <s>👩‍🦳 "Does not have permission to delete"</s> (we're not checking this properly)
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
# > Use `PUT` and not `PATCH` to be explicit with missing values!
# 
# Here's the old `PATCH` update route (using `SQLModel`) for reference. I feel
# it's generally safer to be explicit, and removes any doubt about supplied data.


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
