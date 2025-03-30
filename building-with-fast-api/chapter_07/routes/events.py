from fastapi import APIRouter, Body, Depends, HTTPException, Request

from auth.authenticate import authenticate
from database.connection import get_session
from models.events import Event, EventUpdate
from sqlmodel import select, delete

from typing import List

# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Use a response type when you want to return the full model type. You can use
# `response_model=` (always prioritised if used) if there's sensitive information
# and you need to send a slightly different model type than you received (such as
# a password field).
#
# Error messages
# --------------
# > ⚠️ Error messages for Pydantic and SQLModel can be a bit cryptic.
#
# In general Python error messaging is way worse than Elm Lang. In future aim to use a
# programming language that is EXCELLENT at error messages (many throw errors
# that are too hard to understand!)
# 
# Boring technology
# -----------------
# > ⚠️ Where possible use BORING technology.
# SQLModel is bleeding edge and therefore a risk.
#
# UI and User Experience
# ----------------------
# > ⚠️ Wherever you `DELETE` data, be sure to prompt the user to confirm.
#
# Authentication
# --------------
# > ⚠️ Be sure to authenticate "risky" routes ...
# > The `authenticate` function is used to check if a user is logged in.
# > It'll return the user's email address if they are (from the `payload`)!
# 
# These are things that should not be public facing, or possible to do
# without an account. Also make sure that the _correct user_ is allowed to edit
# _their_ posts, but not posts of other users.
#
# Questions
# ---------
# 1. ⭐ Visually describe what `Depends()` does.
# 2. ⭐ Understand what a path, query, request parameters are.
# 3. ⭐ I think we could use `EventUpdate(BaseModel)` here
#    - And manually unpack it's contents instead of using `data.model_dump()`
# 4. Is `session=` just a named attribute? (custom)
# 5. Understand why `data.model_dump(exclude_unset=True)` is used.
#    - This used to be `data.dict` which is now deprecated
#    - We're now using `PATCH` instead of `PUT` (partial updates)
#    - @ https://sqlmodel.tianglo.com/tutorial/fastapi/update
# 6. Why does `count()` fail with SQLModel? (has no attribute 'count')
#    - Using `.first()` or `.one()` is the recommended way to get a single row
#    - https://github.com/fastapi/sqlmodel/issues/280
#    - https://sqlmodel.tiangolo.com/tutorial/one/
# 7. Am I deleting all `Event` rows correctly?
# 8. Is `Body()` necessary here? (I don't think so)
#    - I think the same goes for `Request()`
#    - Keep your code clean and simple!
# 9. Why do some examples use `await` and others don't?
#    - SQLite is synchronous, so we don't need `await` here!
#    - `await` is used for asynchronous code (like web requests)
#
# Bugs
# ----
# 1. ⭐ Duplicate `:id`s cause errors with SQL `POST`
#    - Solution 1: Use a UUID instead of an integer
#    - Solution 2: Check for duplicates before adding to the database
# 2. Make sure all errors are handled.
#    - See `chapter_03` for full checks, such as `[]` empty events, and
#      duplicate `:id`s in the "database".
#    - Map this out visually using potential inputs, but don't over plan!
# 3. ⭐ Currently ANY authenticated user can update ANY event:
#    - You should always check that an event "belongs" to the current user.

event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# Routes -----------------------------------------------------------------------
# 1. `Depends()` runs the `get_session()` function first (opens a session)
# 2. `Event` is now an `SQLModel` type (it's a table)
# 3. `.session.exec()` executes the supplied `statement`
# 4. Other commands are the same as before (add, commit, refresh)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event) #! 'SELECT * FROM Event' I think?
    events = session.exec(statement).all() # Execute the statement
    return events # FastApi will convert `Event` objects to JSON

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    raise HTTPException(
        status_code=404,
        detail=f"Event with ID: {id} does not exist"
    )


@event_router.post("/new")
#! Body() isn't needed? async def create_event(body: Event = Body(), session=Depends(get_session)) -> dict:
async def create_event(body: Event, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    body.creator = user # Make the user (email) the creator of the event
    session.add(body) # Use the body argument with `Event` type
    session.commit() # Commit the `Event` to the database
    session.refresh(body) #! Refresh the `Event` object

    return {
            "message": "Event created successfully",
            "user": user, #! Debugging only: this will return the user's email!
            "event": body #! Debugging only: this will return the `Event` object
            }

#! We've changed from `PUT` to `PATCH` here (see tag `1.10.4`, deprecated)
@event_router.patch("/edit/{id}", response_model=Event)
async def update_event(id: int, data: EventUpdate, user: str = Depends(authenticate), session=Depends(get_session)) -> Event:
    event = session.get(Event, id) # Get the `Event` object from database

    if not event:
        raise HTTPException(status_code=404, detail="Event not found!")
    
    #! Positively check or negatively check?
    if event.creator != user:
        raise HTTPException(
            status_code=400,
            detail="You can only update events that you've created"
        )

    event_data = data.model_dump(exclude_unset=True) # Using our `EventUpdate` body
    event.sqlmodel_update(event_data) # Update `Event` object with request body data
    session.add(event)
    session.commit()
    session.refresh(event)

    return event # You MUST return something (or you'll get an `Internal Server Error`)


@event_router.delete("/{id}")
async def delete_event(id: int, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    event = session.get(Event, id)

    #! Positively check or negatively check?
    if event.creator != user:
        raise HTTPException(
            status_code=404,
            detail="Event not found" #! This is a lie, but it's more secure
        )

    if event:
        session.delete(event)
        session.commit()
        return { "message": f"Event with ID: {id} has been deleted!" }
    
    raise HTTPException(
        status_code=404,
        detail=f"Event with supplied ID {id} does not exist"
    )

#! DANGER! Warn the user (see notes)
@event_router.delete("/")
async def delete_all_events(session=Depends(get_session)) -> dict:
    events = session.exec(select(Event)).first() # See if there are any events

    if events == None:
        raise HTTPException(status_code=404, detail="Event list already empty")
    
    statement = delete(Event)
    result = session.exec(statement)
    session.commit()
    rows = result.rowcount # How many rows were deleted? (debugging)

    return { "message": f"Deleted {rows} rows this time"}
