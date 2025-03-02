from auth.hash_password import HashPassword
from database.connection import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User, UserSign
from sqlmodel import select

# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# ⚠️ We're exposing `password` as plain text here, these should ALWAYS be hashed
# encrypted in production. We'll cover this in chapter 06.
#
# Wishlist
# --------
# 1. What about `+test` type email addresses?
#    - Should these be disallowed?
# 2. Which encryption package is best?

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)

# Database ---------------------------------------------------------------------
# When we're adding a user to the database, we need to give them a unique ID.
# Before we were allocating the email as the ID (which is a bad idea). Our data
# structure used to look like this: `{"user@email": User(...)}`

users = {}

# Hashing password -------------------------------------------------------------
# We're using a `HashPassword` class to hash our passwords.

hash_password = HashPassword()

# Routes -----------------------------------------------------------------------
# Our database users should have a unique ID, which is a number or UUID. We'll
# create this automatically and use our `User.email` to check against on sign-up.
#
# 1. #! This feels a bit fragile. As our `User.events` is optional, we could've
#    submitted a `User` in our json body (and ommitted the events)

@user_router.post("/signup")
async def sign_new_user(data: UserSign, session=Depends(get_session)) -> dict:
    # First check if user already exists
    statement = select(User).where(User.email == data.email)
    user = session.exec(statement).first()
    
    if user: # This could be `None` if user doesn't exist
        raise HTTPException(status_code=409, detail="Username already exists")

    # Hash the password (using `data` which is a `UserSign` class)
    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password

    # Now add the user with their newly hashed password
    session.add(User(email=data.email, password=data.password)) #! (1)
    session.commit()

    return { "message": f"User with {data.email} registered!" }

@user_router.post("/signin")
async def sign_in_user(user: UserSign, session=Depends(get_session)) -> dict:
    # First check if user already exists
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if db_user.password != user.password:
        # Search Brave Ai answer for "403 vs 401 wrong password"
        raise HTTPException(status_code=401, detail="Invalid password")
    
    #! We aren't doing any authentication right now, but can pretend we're
    # storing some useful session data and return it (for testing purposes)
    users[user.email] = db_user
    
    return {
        "message": "User signed in successfully!",
        "signed in": users
    }
