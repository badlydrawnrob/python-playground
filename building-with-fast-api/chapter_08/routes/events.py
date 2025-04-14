from fastapi import APIRouter, Body, Depends, HTTPException

from auth.authenticate import authenticate
from database.connection import sqlite_db
from database.models import EventData, UserData
from models.events import Event, EventUpdate, EventJustTitle

from playhouse.shortcuts import model_to_dict

from typing import List

# ------------------------------------------------------------------------------
# Our EVENTS routes
# ==============================================================================
# Here we setup our app routes. We're using our Pydantic or SQLModel models.
# If there's sensitive information in the model, we can use `response_model=` to
# return a different model type (sans sensitive information). SQLModel is bleeding
# edge and a bit of a risk. Use boring technology where possible.
#
# Warning
# -------
# > PeeWee isn't compatible with `async` by default ...
# > See `database.connection` for how to fix this ...
# 
# For now, we'll remove the `async` from FastApi, which kind of defeats the
# purpose, but it'll do for a thousand users, and we can change our ORM later
# to an async one, or fix the connection with PeeWee.
#
#
# Questions
# ---------
# > ⭐ How many concurrent connections can SQLite handle?
#
# 1. What's preferrable, `get()` or `get_or_none()`?
#    - The latter is more similar to SQLModel and can be checked for `None`
#    - The former (I think) requires a `try/except` block, which I don't prefer
#      @ https://softwareengineering.stackexchange.com/a/107727
# 2. Understand the difference between a response type and a `response_model=`
#    - And why `response_model=` is used in some cases and not others.
#    - `response_model=` is always prioritised if used.
# 3. ⭐ Visually describe what `Depends()` does.
# 4. ⭐ Understand what a path, query, request parameters are.
# 5. Understand named keyword arguments (`session=Depends(get_session)`)
# 6. Why `data.model_dump(exclude_unset=True)`?
#    - This removes any `None` values that haven't been set.
#    - `data.dict()` is deprecated
# 7. Why `PATCH` instead of `PUT`? (see tag `1.10.4`)
#    - @ https://sqlmodel.tianglo.com/tutorial/fastapi/update
# 8. Don't need to understand them, but know that `Body()` and `Request()` exist.
# 9. SQLite doesn't really allow `await`, but understant it exists. (AsyncIO)
# 10. Understand that a `PATCH` call could have any number of `Optional` fields
#    that have not been set.
#    - How does this affect our DATA models. Do we want to use `PUT` instead?
#    - With `PATCH` there's no way of knowing which data is present, so we'd need
#      PeeWee to be flexible with it's update function (I think we can just change
#      the fields in the object `User.name = "Name"`)
# 11. Using `PUT` instead of `PATCH` (following on from Q6 and Q11)
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
# 1. Fix the `session=Depends(get_session)` problem. We're not abstracting with
#    PeeWee and have to `db.connect()` and `db.close()` for every route!
#    - Add this to `database.connection` later, if it's possible (commit `1.12.7`)
# 2. Some routes use `user: str = Depends(authenticate)` to get the user
#
# > Admin and roles
#
# 1. We need to add a role to the user (e.g: admin, user, etc)
# 2. `DELETE` all events is a destructive action, which should be admin only!
#    - I've removed this route from the app. Use raw SQL instead.
#    - That's a lot simpler and SAFER!!! There's no way to accidentally delete.
#    - You might like to use a GUI, or a no-code dashboard.
# 3. ⭐ How to `EventData.save()` and store the data before `.close()`?
#    - You've got to be careful where you place your `db.close()` function.
#    - Remember your object will look like `<Person 1>` which is an OBJECT,
#      NOT DATA! ... pull out data with `model_to_dict()` and _then_ `.close()`

event_router = APIRouter(
    tags=["Events"] # used for `/redoc` (menu groupings)
)


# Routes -----------------------------------------------------------------------
# 1. `Depends()` runs before the route function
# 2. `Event` is now an `SQLModel` type (is it a table?)
# 3. `.session.exec()` executes the supplied `statement`
# 4. You'll also need to understand the other commands (add, commit, refresh)

@event_router.get("/", response_model=List[EventJustTitle])
def retrieve_all_events() -> List[EventJustTitle]:
    """Return a simple list of event titles
    
    A little different than our book example, but just to show the flexibility
    and speed of a Pythonic solution. I generally type in an Elm-style, but this
    is quite graceful!
    """
    sqlite_db.connect()

    query = EventData.select() #! 'SELECT * FROM Event'
    events = [user.title for user in query] # List comprehension

    sqlite_db.close()

    return events


@event_router.get("/{id}", response_model=Event)
def retrieve_event(id: int) -> Event:
    sqlite_db.connect()
    event = EventData.get_or_none(EventData.id == id) #! See (1) in Qs

    if event:
        return model_to_dict(event)
    
    # Should alway close connection OUTSIDE of the `if` statement?
    # unless the connection is opened within the `if` ... but should
    # it come after the `raise`? I don't like `try/except/finally` blocks
    # which is the other option (`finally` closes the connection)
    sqlite_db.close()

    raise HTTPException(
        status_code=404,
        detail=f"Event with ID: {id} does not exist"
    )


@event_router.post("/new")
def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    """Create a new event
    
    Our `Depends(authenticate)` function will run before this route, and will
    fail if user is not logged in. There's no need to check that again within the
    body function.

    The `user` value should really be a `nanoid`, which we use to reference the
    user in the database, and do any real work with `User.id` (a simple
    incrementing `int`. However ...

    We may as well let PeeWee do the work for us, and just supply a `User` object,
    and it'll extract the `id` for us. This feels a bit icky to me coming from
    a statically typed (I'd rather explicitly set the `id`), but it works.
    """    
    sqlite_db.connect()
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
    
    event = model_to_dict(query)
    sqlite_db.close()

    #! Debugging only: we don't need to return `user` or `body`
    #! I think `query` requires a PROPER `USER` rather than a simple
    #! `id` integer value, as `event` below throws an error ...
    #! `database.models.UserDataDoesNotExist` ...
    #! or I'm trying to use the `email` for Event.creator rather than
    #! `User.id` which I think it's expecting ...
    #!
    #! So I think I've gotta grab the user (from email) create the user
    #! object and then generate the query. Alternatively, just use the email
    #! as the foreign key (but you'll likely get `<Event None>` because it expects
    #! a `User` OBJECT
    #!
    #! Not a huge fan of having to use objects in this way. Easier just a record id.
    return {
            "message": "Event created successfully",
            "user": user,                #! Debug
            "event": event #! Debug
            }


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
