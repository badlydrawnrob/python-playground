from fastapi import APIRouter, Body, Depends, HTTPException, Request

from database.connection import get_session
from models.events import Event, EventUpdate
from sqlmodel import select

from typing import List

# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Once again `response_model=` (seems) to be used when we want a different
# response back from the server than the input json body ... for example,
# removing sensitive data from the response. We're now using SQLModel (or MongoDB)
# to format our `Event` models.
#
# Questions
# ---------
# 1. Why would we use `response_model=` when we already have a response type?
#    - I think that FastApi will always prioritise the `response_model=`
# 2. What is `Body()` and how does it work?
#    - ⚠️ `Body()` here is not necessary as we're already using Pydantic model
#    - @ https://stackoverflow.com/a/56996770
#    - @ https://fastapi.tiangolo.com/tutorial/body/
# 3. What do `Depends()` and `Request()` do?
#    - Show how `Depends()` creates the `session=` and explain `yield`
#    - The dependency condition (the function) must be satisfied before any
#      operation can be executed.
#    - Basically (what I think this means is) that an session MUST be opened,
#      before any of the function code can be executed.
#    - Is there a more functional way of doing this?
# 4. Lookup path, query, and request parameters:
#    - To understand things like `session=` and `response_model=`
#    - @ https://gpttutorpro.com/fastapi-basics-path-parameters-query-parameters-and-request-body/
# 5. `data.dict` is deprecated, but what's `exclude_unset=`?
#    - THE EXAMPLE DOCUMENTATION USES `PATCH`, so just use `PATCH`!
#    - See @ https://sqlmodel.tianglo.com/tutorial/fastapi/update
#    - `setattr()` also needs explaining, as does it's params
# 6. #! The example code folders use `await` keyword.
#    - Is this a necessity?
#
# Bugs
# ----
# 1. Duplicate `:id`s cause errors with SQL `POST`

event_router = APIRouter(
    tags=["Events"]
)

# Events DB --------------------------------------------------------------------
# 📆 We start to use a PROPER `Event` table for our storage. See `models.events`!

# events = []

# Routes -----------------------------------------------------------------------
# != See `chapter_03` for full checks. We're ignoring some checks here, such
# as `[]` empty events, if event `id` is a duplicate, and so on.
#
# 1. Use `Depends()` to create a session
# 2. Use Pydantic to format the `Event` model
# 3. Add an `Event` and `.commit()` it to the database (make sure to `.refresh()`)
# 4. Grab all `Event`s with a `SELECT` statement with `session.exec()`

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event) #! The SQL statement, 'SELECT * FROM Event' I think?
    events = session.exec(statement).all() # Execute the statement within session (all rows?)
    return events

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
async def create_event(
    body: Event = Body(), #! Body() is not needed here (see notes)
    session=Depends(get_session) #! I think this is a named attribute?
    ) -> dict:
    session.add(body)     # Pull object
    session.commit()      # Commit and FLUSH
    session.refresh(body) #! Refresh the database? How does this work?

    return { "message": "Event created successfully" }

#! You could also use `PATCH` here (which might be preferrable partial updates)
@event_router.patch("/edit/{id}", response_model=Event)
async def update_event(id: int, data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id) # We use the `Event` model to GET the event from DB ...
    # See tag `1.10.4` for deprecated version
    if not event:
        raise HTTPException(status_code=404, detail="Event not found!")
    event_data = data.model_dump(exclude_unset=True) # Our `EventUpdate` body
    event.sqlmodel_update(event_data) # Update `Event` with `EventUpdate` data
    session.add(event)
    session.commit()
    session.refresh(event)
    # Make sure you return something or you'll get `Internal Server Error`
    return event

@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {
            "message": f"Event with ID: {id} has been deleted!"
        }
    raise HTTPException(
        status_code=404,
        detail=f"Event with supplied ID {id} does not exist"
    )

# @event_router.delete("/")
# async def delete_all_events() -> dict:
#     if len(events) == 0:
#         raise HTTPException(status_code=404, detail="Event list already empty")
    
#     events.clear()
#     return { "message": "Events deleted successfully" }
