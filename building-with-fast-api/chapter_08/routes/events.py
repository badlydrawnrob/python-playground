from fastapi import APIRouter, Body, Depends, HTTPException, Request

from auth.authenticate import authenticate
from database.connection import get_session
from models.events import Event, EventUpdate
from sqlmodel import select, delete

from typing import List

# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Here we setup our app routes. We're using our Pydantic or SQLModel models.
# If there's sensitive information in the model, we can use `response_model=` to
# return a different model type (sans sensitive information). SQLModel is bleeding
# edge and a bit of a risk. Use boring technology where possible.
#
# Questions
# ---------
# > How many concurrent connections can SQLite handle?
#
# 1. Understand the difference between a response type and a `response_model=`
#    - And why `response_model=` is used in some cases and not others.
#    - `response_model=` is always prioritised if used.
# 2. ⭐ Visually describe what `Depends()` does.
# 3. ⭐ Understand what a path, query, request parameters are.
# 4. Understand named keyword arguments (`session=Depends(get_session)`)
# 5. Why `data.model_dump(exclude_unset=True)`?
#    - `data.dict()` is deprecated
# 6. Why `PATCH` instead of `PUT`? (see tag `1.10.4`)
#    - @ https://sqlmodel.tianglo.com/tutorial/fastapi/update
# 7. "SQLModel has no attribute 'count'"
#    - Using `.first()` or `.one()` is the recommended way to get a single row
#    - @ https://github.com/fastapi/sqlmodel/issues/280
#    - @ https://sqlmodel.tiangolo.com/tutorial/one/
# 8. We're often using the `SQLModel` class to access/input data:
#    - e.g: `statement = delete(Event)`
#    - Understand this a little deeper (core ORM concepts)
# 9. Don't need to understand them, but know that `Body()` and `Request()` exist.
# 10. SQLite doesn't really allow `await`, but understant it exists. (AsyncIO)
# 11. Can we use `session.add()` instead of `.sqlmodel_update()`?
#    - `.sqlmodel_update()` is a method of `SQLModel` that updates the object,
#      but it's pretty hard to find in the documentation.
#    - Alternatively you could provide all values explicitly, then use `.add()`
#      as you would when creating a new event. This might not work too well as
#      there's no way to know _which_ data is present (because it's a `PATCH`).
# 12. Using `PUT` instead of `PATCH` (following on from Q6 and Q11)
#    - Using `.add()` would be better with a `PUT` where all data is present.
#    - @ https://fastapi.tiangolo.com/tutorial/body-updates/#update-replacing-with-put
#    - @ https://sqlmodel.tiangolo.com/tutorial/update/#add-the-hero-to-the-session
#
#
# The user experience
# -------------------
# 1. Whenever you `DELETE` data, be sure to prompt the user to confirm.
# 2. Make sure to handle errors correctly. Don't leak sensitive information.
# 3. Authenticate all routes that require authentication, or are "risky".
#    - These are anything that should not be public-facing.
#    - We use the `Depends(authenticate)` function for this. Returns @email.
#    - Make sure it's the correct user that is allowed to edit their posts.
#
# Bugs
# ----
# 1. ⭐ Duplicate `:id`s cause errors with SQL `POST`
#    - FastApi auto-increments so just ommit the `:id` field from the request
#    - You could also use a `UUID` instead of an integer
# 2. Make sure all errors are handled
#    - See `chapter_03` for full checks, such as `[]` empty events, etc
#    - Have a high-level view of your API (Bruno is a good start)
#
# Wishlist
# --------
# > Securing routes
# 
# Set these all in one place? Search Brave with "fastapi always run the session"
#
# 1. All routes use `session=Depends(get_session)` to get a database session
# 2. Some routes use `user: str = Depends(authenticate)` to get the user
#
# > Admin and roles
#
# 1. We need to add a role to the user (e.g: admin, user, etc)
# 2. `DELETE` all events is a destructive action, which should be admin only!
#    - I've removed this route from the app. Use raw SQL instead.
#    - That's a lot simpler and SAFER!!! There's no way to accidentally delete.
#    - You might like to use a GUI, or a no-code dashboard.

event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# Routes -----------------------------------------------------------------------
# 1. `Depends()` runs before the route function
# 2. `Event` is now an `SQLModel` type (is it a table?)
# 3. `.session.exec()` executes the supplied `statement`
# 4. You'll also need to understand the other commands (add, commit, refresh)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event) #! 'SELECT * FROM Event'
    events = session.exec(statement).all() # Run statement
    return events # FastApi converts `Event` objects to JSON automatically

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
async def create_event(body: Event, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    body.creator = user # `User` email is creator of event
    session.add(body) # `Event` type added to session
    session.commit() # Commit `Event` to the database
    session.refresh(body) #! Refresh the `Event` object

    #! Debugging only: we don't need to return `user` or `body`
    return {
            "message": "Event created successfully",
            "user": user, #! Debug
            "event": body #! Debug
            }

@event_router.patch("/edit/{id}", response_model=Event)
async def update_event(id: int, data: EventUpdate, user: str = Depends(authenticate), session=Depends(get_session)) -> Event:
    event = session.get(Event, id) # Get `Event` object from database

    if not event: # is `None` if event doesn't exist
        raise HTTPException(status_code=404, detail="Event not found!")
    
    #! Positively check or negatively check? (preference)
    if event.creator != user: # Check if user is creator of event
        raise HTTPException(
            status_code=400,
            detail="You can only update events that you've created"
        )

    event_data = data.model_dump(exclude_unset=True) # EventUpdate(BaseModel) could be used instead
    event.sqlmodel_update(event_data) # Update new `Event` object (see Q11)
    session.add(event)
    session.commit()
    session.refresh(event)

    return event # If you don't return something you'll get `Internal Server Error`!


@event_router.delete("/{id}")
async def delete_event(id: int, user: str = Depends(authenticate), session=Depends(get_session)) -> dict:
    event = session.get(Event, id)

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

#! See WISHLIST above. Removed route to delete all events ...
#! With `sqlite3 planner.db` in terminal `DELETE FROM event;`
