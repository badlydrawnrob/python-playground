# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Our app routes use Pydantic for API data validation and Piccolo ORM for our
# data models. SQLite is not strict by default, so we've got to be extra careful.
# If there's sensitive information we don't wish to expose, we can use the
# `response_model=` with the correct Pydantic model.
#
#
# Async only
# ----------
# > Beware of routes that contain both read and write functions!
#
# For atomic data (for now) it's much easier for any update/insert/delete function
# NOT to also contain reads within the same endpoint. Otherwise you get the same
# "database locked" problem we had with PeeWee, which has to be handled by changing
# the transaction type.
#
#     @ https://piccolo-orm.readthedocs.io/en/latest/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html
#     @ https://github.com/piccolo-orm/piccolo/issues/1319
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
# 1. `Depends(authenticate)` runs before the route function
#     - It fails if user is not logged in
# 2. Use a Pydantic `-> Response` type -or- `response_model=`
#     - You generally do not want (or need) to use both!
#
#
# Questions
# ---------
# 1. How best to check for `None` or `[]`?
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
# 1. Event creator should be `User.id` not `User.email`
# 2. We no longer have sessions (SQLite doesn't need them) - remove.
# 3. Assure all routes that need authentication have it with
#     - `user: str = Depends(authenticate)`
# 4. Are there any obvious errors we're not handling?
#     - Write a duplicate ID function (SQLite unique constraint error)
# 5. Remove ALL documentation from Bruno
#     - Follow the "APIs you won't hate" guidelines
#     - Bruno could be the "high level viewpoint" of your API?
# 6. Write a brief note about the difference between response type ...
#     - And `response_model=` ... and which to prefer
#     - `response_model=` is always prioritised if used.
# 7. Write an article about making `/signup` more graceful with Piccolo:
#    - How does it effect usability and the user experience? (Artifacts)
#    - Option 1: Have a simple "invite" process and manually create accounts
#    - Option 2: Find a professional and delegate the process
#        - Just how much would this cost? (via Ai / via Human)
#        - Signup -> Email -> Verify (code) -> Login -> Onboarding
# 8. Create different `include_router` packages for authentication routes?
#    - @ https://fastapi.tiangolo.com/tutorial/bigger-applications/
#    - @ https://stackoverflow.com/a/67318405

from auth.authenticate import authenticate
from fastapi import APIRouter, Body, Depends, HTTPException

from planner.tables import Event
from planner.models.events import Event, EventUpdate, EventJustTitle, EventWithCreator

from typing import List

event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# Routes -----------------------------------------------------------------------

@event_router.get("/", response_model=List[EventJustTitle])
def retrieve_all_events() -> List[EventJustTitle]:
    """Return a simple list of event titles!
    
    A little different than our book example, but just to show the flexibility
    and speed of a Pythonic solution. I generally type in an Elm-style, but this
    is quite graceful!
    """
    sqlite_db.connect()

    query = EventData.select() #! 'SELECT * FROM Event'
    events = [{"title": user.title} for user in query] # List comprehension

    sqlite_db.close()

    return events


@event_router.get("/{id}", response_model=Event)
def retrieve_event(id: int) -> Event:
    """Retrieve a single event by ID
    
    Should we always close connection OUTSIDE of the `if` statement? PeeWee holds
    on to the object, even if the connection has been closed. I guess the next
    call will recycle the `event` variable (Python is mutable).

    I don't like `try/except/finally` blocks (`finally` closes the connection),
    so we're avoding that with the `get_or_none()` function, which makes behaviour
    similar to SQLModel.
    
    Otherwise we get a big exception we'd need to deal with, if there are no
    results for the database query.
    """
    sqlite_db.connect()
    event = EventData.get_or_none(EventData.id == id) #! See (1) in Qs

    if event:
        return model_to_dict(event)
    
    sqlite_db.close()

    raise HTTPException(
        status_code=404,
        detail=f"Event with ID: {id} does not exist"
    )


@event_router.post("/new")
def create_event(
    body: Event,
    user: str = Depends(authenticate)) -> EventWithCreator:
    """Create a new event

    The `user` value should really be a `nanoid`, which we use to reference the
    user in the database, and do any real work with `User.id` (a simple
    incrementing `int`. However ...

    We may as well let PeeWee do the work for us, and just supply a `User` object,
    and it'll extract the `id` for us. This feels a bit icky to me coming from
    a statically typed (I'd rather explicitly set the `id`), but it works.
    
    Speed
    -----
    > ⚠️ The first time I ran this function, it was pretty slow ...
    
    Subsequent calls were much faster. I don't know why this is.
    """    
    sqlite_db.connect(reuse_if_open=True) #! ⚠️ This feels a bit BRITTLE!
    username = UserData.get(UserData.email == user) #! Create a `UserData` object

    # Our `EventData.id` field is auto-generated by PeeWee and not set in our 
    # `Event` request body, so ... `User`` either `exclude_none=True` or the
    # setting below. Also, our `PeeWee` type `EventData` will need a proper
    # `UserData.id` value. It's not strict by default, and the book uses an
    # `EmailString` value.
    # 
    # Even though PeeWee should stop our `Event.creator` (an `int` value) from
    # submitting, it doesn't. SQLite accepts whatever you give it by default ... 
    # ANY data. Any data at all. In order to force strictness, we need to set our
    # tables to `strict` mode. Postgres doesn't have this problem (always strict).
    #
    # @ https://sqlite.org/stricttables.html
    # 
    query = EventData(creator=username, **body.model_dump(exclude_none=True))
    query.save() # You could've used `EventData.create(**kwargs)` instead
    
    sqlite_db.close()

    #! Debugging ONLY. NEVER expose sensitive details in production.
    #!
    #! In order to hide our `UserData.email` and `UserData.password`,
    #! (I think) we MUST do this manually, unlike SQLModel, which can
    #! have a model that excludes sensitive data.
    #!
    #! We could also use FastApi's `response_model=` to exclude sensitive data.
    #! Preparing for other frameworks however, it's not a bad idea to do things
    #! manually, as I imagine OCaml and Elm would do it like that. 

    return model_to_dict(query) # You could write this _before_ `close()`


"""
********************************************************************************
A user profile with user details and all their (only their) events route
********************************************************************************
"""

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


@event_router.delete("/{id}")
def delete_event(id: int, user: str = Depends(authenticate)) -> dict:
    event = EventData.get(EventData.id == id)

    if event.creator != user:
        raise HTTPException(
            status_code=404,
            detail="Event not found" #! This is a lie, but it's more secure
        )

    if event:
        row = event.delete_instance()

        return { "message": f"{row} Event deleted with ID# {id}!" }
    
    raise HTTPException(
        status_code=404,
        detail=f"Event with supplied ID {id} does not exist"
    )

#! See WISHLIST above. Removed route to delete all events ...
#! With `sqlite3 planner.db` in terminal `DELETE FROM event;`
