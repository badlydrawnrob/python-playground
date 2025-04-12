from auth.authenticate import authenticate
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token

# from database.connection import get_session
from database.connection import sqlite_db
from database.models import UserData, EventData

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from models.users import User, TokenResponse
from models.events import Event

# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# > ⭐ Our `User` routes should be treat like a black box.
# > See `chapter_07` for more details on the authentication functions.
# 
# Our password hashing, authentication, and other functions can be treated as a 
# "black box", where we hire a professional to worry about that for us, and all
# we've got to do is write our `Depends(authenticate)` and hashing methods and
# not worry about it! No need to understand what `Oauth2PasswordRequestForm` is.
#
# Our user has an `email` and `password`. The `username` is their `email`. You
# should have a high-level view of how this works:
#    @ https://tinyurl.com/fastapi-oauth2-depends
#
#
# Invite only
# -----------
# > Building a proper authentication system is hard.
# > We're currently using JWT Bearer tokens (in the header).
#
# Your app could be invite-only, and you manually create the user accounts on
# their behalf. If you need a fully fledged authentication system, you'll have to
# look elsewhere, as our `/signup` route isn't fully secure (no email verification).
#
#
# Wishlist
# --------
# 1. We should probably disallow `+test` type email addresses.
#    - Although these are useful for testing.
# 2. The expiry time is currently hard-coded to 1 hour.
#    - Should this be an `.env` variable setting?
#    - We need to write a function to extend the expiry time.
# 3. Do we need a separate `User` and `UserSign` class?
#    - Otherwise all our `User`s will have `Optional` (`None`) fields.
# 4. Fix the `session=Depends(get_session)` problem. We're not abstracting with
#    PeeWee and have to `db.connect()` and `db.close()` for every route!
#    - Add this to `database.connection` later, if it's possible (commit `1.12.7`)
# 5. We could've used a `TypedDict` here, but `response_model=` converts our `dict`
#    to a `TokenResponse`, which is slightly cleaner.
# 6. How do we make sure PyLance recognises our types?
#    - PeeWee `Field` typing is a bit off for `.get()` and `.create()`
#    - It's also not recognising our `UserData` field types on retrieval.
#
# Not my job
# ----------
# 1. Are there better encryption methods than `python-jose`?
# 2. Hashing can be slow. Can it be speeded up?


user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)

# Hashing password -------------------------------------------------------------

hash_password = HashPassword()

# Routes -----------------------------------------------------------------------
# Here we're converting from FastApi Pydantic (API layer) to PeeWee (Database layer)

@user_router.post("/signup")
def sign_new_user(data: User) -> dict:
    """Convert `User` -> `UserData` object, then add it to the database."""
    sqlite_db.connect()
    user = UserData.get(UserData.email == data.email) # Does user exist?
    
    if user: # `None` if user doesn't exist
        raise HTTPException(status_code=409, detail="Username already exists")

    # Secure the password and replace `User.password` with hash
    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password

    # Add user to database (`User` -> `UserData`)
    # 1. Convert `User` to a dictionary (excluding `None` key/values)
    # 2. Create a `UserData` object (with `**kwargs`)
    # 3. Save it to the database (similar to SQLModel's `commit()`)
    new_user = UserData.create(**data.model_dump())
    new_user.save() # should return `1` affected row

    #! Close the connection (4)
    sqlite_db.close()

    return { "message": f"User with {new_user.email} registered!" }


@user_router.post("/signin", response_model=TokenResponse) #! dict -> model (5)
def sign_in_user(data: OAuth2PasswordRequestForm = Depends()):
    """Checks if: `User` exists? correct details? Return `token`
    
    #! Types are a bit fucked up as `Oauth...` is used, and it doesn't
       know which type it is.
    """
    sqlite_db.connect()
    user = UserData.get(UserData.email == data.username)

    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    if hash_password.verify_hash(data.password, user.password):
        access_token = create_access_token(user.email) #! Change to `public` id

        return {
            "access_token": access_token, # (5)
            "token_type": "Bearer"
        }
    
    # `UserData` exists but hashed password isn't working
    # Search Brave for "403 vs 401 wrong password"
    raise HTTPException(status_code=401, detail="Invalid password")


@user_router.get("/me")
def get_user_me(user: str = Depends(authenticate)):
    """Get all `Event`s with the `UserData.id` joined on
    
    I struggled to understand this with SQLModel, which is the main reason
    I switched over to PeeWee (taking the hit on no `async` functionality).
    The raw SQL query should look something like this:

    ```sql
    SELECT * FROM event
    JOIN user ON event.creator = user.email
    WHERE event.creator = 'lovely@bum.com';
    ```

    You can use raw SQL with PeeWee if you like, but we'll do it the safe way.
    """




    # (1) Selecting `User` and `Event` columns
    # ----------------------------------------
    # This is the first part of documentation here:
    # You're basically returning a `Tuple` of `(User, Event)` objects that
    # match the user's email. In SQL it'd look like:
    #
    # `cdb194405db64ffeaed9c82ee1b49253|lovely@bum.com|1|lovely@bum.com` etc
    #
    # Notice the duplication there? That's because it isn't a proper join.
    #
    # ```
    # statement = select(User, Event).where(Event.creator == user)
    # results = session.exec(statement).all()
    # ```
    #
    # The problem is these haven't been serialised as json yet. You could use
    # `response_model=` but I'm not sure how that should look. Or, you can create
    # another model for the response, but that seems like A LOT of work to do
    # for every join.
    #
    # The alternative is to convert the rows to json.
    #
    # (2) Second attempt using a `join`
    # --------------------------------------------------------------------------
    # This version is using a join, but I can't figure out how the fuck to get
    # back what I want, which is the `Event` rows with `Event.creator` joined
    # onto the `User` details. Do I have to create another `models.event` for this?
    # See `EventWithUser`: what do I put here?
    #
    # ```
    # statement = select(Event, User).join(User).where(Event.creator == user)
    # results = session.exec(statement).all()
    # ```
    # The code above currently outputs:
    #
    # ('lovely@bum.com',)
    #
    # Calling `results` again reveals it's type:
    # `<sqlalchemy.engine.result.ChunkedIteratorResult object at 0x103fa3d00>`
    #
    # @ https://stackoverflow.com/a/78832114
    # Which should be callable with `all()`, `first()`, or `one()`
    #
    # However it RETURNS NO RESULTS, just an empty `[]` list.
    #
    # The docs say we shouldn't need to use `ON` keyword, as it's inferred by
    # `foreign_key=` in the `models.events` package ... but we get nothing!
    #
    # FYI, in SQL it'd look something like:
    #
    # ```
    # SELECT * FROM event
    # JOIN user ON event.creator = user.email
    # WHERE event.creator = 'lovely@bum.com';
    # ```
    # 
    # Which DOES return something (split onto new lines):
    #
    # ```
    # 1|lovely@bum.com|Glastonbury|https://somegood.com/song.jpg|
    # Ed Sheeran singing his best song 'Class A Team'!|Live|["music", "adults", "event"]|
    # cdb194405db64ffeaed9c82ee1b49253|lovely@bum.com|$2b$12$25mRszZMp71Gulk3sFHyRundN7WeKLp.AnUJGSvp2xHxQNGMVnJFm
    # ```
    #
    # (3) Third attempt (a basic `join`)
    # ----------------------------------
    # > Returns a `List Tuple(Event, User)` object (# of rows depends on DB)
    statement = select(Event, User).join(User) #! How do I narrow down to ONE user?!
    results = session.exec(statement).all()

    # We need to unpack the `Tuple` (why is it a `Tuple`?)
    list = []
    
    for event, user in results:
        list.append(event.title)
        list.append(event.creator)
        list.append(event.tags)
        list.append(user.id)


    #! Currently no guards or error checking!
    return {"data": list}
