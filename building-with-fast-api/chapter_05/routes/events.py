from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Once again `response_model=` (seems) to be used when we want a different
# response back from the server than the input json body ... for example,
# removing sensitive data from the response.
#
# Questions
# ---------
# 1. Why would we use `response_model=` when we already have a response type?
#    - I think that FastApi will always prioritise the `response_model=`
# 2. What is `Body()` and how does it work?

event_router = APIRouter(
    tags=["Events"]
)

# Events DB --------------------------------------------------------------------

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
async def create_event(body: Event = Body()) -> dict:
    events.append(body)

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
