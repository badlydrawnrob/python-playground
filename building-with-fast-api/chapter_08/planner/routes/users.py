# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# > Treat our `User` routes like a "black box"! See `chapter_07` for more info.
# 
# Authentication is difficult, so we hand over this responsibility to Piccolo.
# If you're doing this yourself, it'll take quite a bit of reading and learning.
# You can always hire a professional to worry about this for you. All you need to
# know is that `Depends(authenticate)` checks a user exists and logs them in.
# 
#     @ https://tinyurl.com/fastapi-oauth2-depends
#
# Using Piccolo saves us from a ton of problems that generating our own user's
# with SQLModel or Peewee created. Here's some of your user data:
#
# - `User.username`
# - `User.email`
# - `User.password`
#
#
# Invite only
# -----------
# > Building a proper authentication system is hard!
# > Use JWT Bearer tokens in the request header (be wary of XXS attacks)
#
# A user `/signup` route isn't fully secure as there's no email verification!
#
# Your app could be invite-only and use `piccolo user create` to generate the
# user account. You'd then use `BaseUser.login()` in the sign-in endpoint. For a
# fully fledged authentication system, you'll have to use Piccolo's auth API or
# roll one yourself.
#
#
# Data validation
# ---------------
# > For user data we're using `BaseUser` with Piccolo
#
# This should be automatically handled for us, but you'll still need a Pydantic
# type for the API layer.
#
#
# WISHLIST
# --------
# 1. Use a `TypedDictionary` for the `/signin` response type?

from auth.authenticate import authenticate
from auth.jwt_handler import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from piccolo.apps.user.tables import BaseUser
from planner.models.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)


# ------------------------------------------------------------------------------
# Write routes
# ==============================================================================
# Convert from a Pydantic API type -> Pydantic DATA type

@user_router.post("/signup")
def sign_new_user(data: User) -> dict:
    """Convert `User` -> `UserData` object, then add it to the database.
    
    `.get()` "does this user exist" problem by default throws an exception if
    row doesn't exist. To make it handle similar to SQLModel's `None` if does not
    exist, we use the `get_or_none()` method. Otherwise we get a load of
    traceback error nonsense we have to `try` and catch. Hate `None`, but it's
    easier to work with in this case (rather than `user.exists()`)
    """
    sqlite_db.connect()
    user = UserData.get_or_none(UserData.email == data.email) # Does user exist?
    
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


# ------------------------------------------------------------------------------
# Read routes
# ==============================================================================

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
    
    #! Should this go AFTER the `raise`?
    #! ⚠️ If you don't close this, and your next route ping runs, you'll get a
    #! `Error, database connection not opened` error!
    sqlite_db.close()
    
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

    Converting to `json`
    --------------------
    > @ https://stackoverflow.com/a/58931596 (model -> json)
    > @ https://docs.peewee-orm.com/en/2.10.2/peewee/playhouse.html#shortcuts

    PeeWee has a really handy `model_to_dict()` function (for single records),
    or `.dicts()` for multiple records. For now we'll loop manually, but you
    could get the same result with:

    ```python
    list(bob.pets.dicts())
    ```

    Errors
    ------
    > There's currently not many guards or error checking.

    - We should probably add an "if no user" clause.
    - Our `authenticate()` function raises an error if token isn't valid
    """
    sqlite_db.connect()
    
    # Grab the user again ...
    user = UserData.get(UserData.email == user) #! Change to `public` id
    # Now we can work with the `user` object to get their events.
    user.events #! This is a backref we wrote

    list = []

    for event in user.events:
        e = { "creator": event.creator
            , "event": event.title
            , "tags": event.tags
            }
        
        list.append(e)
    
    sqlite_db.close()

    #! Currently no guards or error checking!
    return {"data": list}
