from fastapi import APIRouter, Body, Depends, HTTPException, Request, status

from database.connection import get_session
from models.events import Event, EventUpdate

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
#    - The dependency condition (the function) must be satisfied before any
#      operation can be executed.
#    - Basically (what I think this means is) that an session MUST be opened,
#      before any of the function code can be executed.
# 4. Lookup path, query, and request parameters:
#    - To understand things like `session=` and `response_model=`
#    - @ https://gpttutorpro.com/fastapi-basics-path-parameters-query-parameters-and-request-body/

event_router = APIRouter(
    tags=["Events"]
)

# Events DB --------------------------------------------------------------------
# 📆 We start to use a PROPER `Event` table for our storage. See `models.events`!

events = []

# Routes -----------------------------------------------------------------------
# != See `chapter_03` for full checks. We're ignoring some checks here, such
# as `[]` empty events, if event `id` is a duplicate, and so on.

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    
    raise HTTPException(status_code=404, detail=f"Event with {id} doesn't exist")

@event_router.post("/new")
async def create_event(
    body: Event = Body(), #! Body() is not needed here (see notes)
    session=Depends(get_session) #! I think this is a named attribute?
    ) -> dict:
    session.add(body)     # Pull object
    session.commit()      # Commit and FLUSH
    session.refresh(body) #! Refresh the database? How does this work?

    return { "message": "Event created successfully" }

@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return { "message": f"Event with {id} deleted" }
    
    raise HTTPException(status_code=404, detail=f"Event with {id} does not exist")

@event_router.delete("/")
async def delete_all_events() -> dict:
    if len(events) == 0:
        raise HTTPException(status_code=404, detail="Event list already empty")
    
    events.clear()
    return { "message": "Events deleted successfully" }
