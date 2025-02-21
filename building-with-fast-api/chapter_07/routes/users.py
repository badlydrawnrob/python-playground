from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSign

# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# ⚠️ We're exposing `password` as plain text here, these should ALWAYS be hashed
# encrypted in production. We'll cover this in chapter 06.

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)

# Database ---------------------------------------------------------------------

users = {}

# Routes -----------------------------------------------------------------------
# Here we'll create our `User()` and access the `.email` field. We'll use that as
# the **primary key** for our `users` dictionary. Currently using `UserSign()`
# for both, rather than creating separate models for `sign-up` and `sign-in`.

@user_router.post("/signup")
async def sign_new_user(data: UserSign) -> dict:
    if data.email in users:
        raise HTTPException(status_code=409, detail="Username already exists")

    users[data.email] = data # != Ask copilot to explain this line
    return { "message": "User registered!" }

@user_router.post("/signin")
async def sign_in_user(user: UserSign) -> dict:
    # Check if `UserSign().email` is in the `users` dictionary
    # You could also use `if _ or _` here!
    if user.email not in users:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if user.password != users[user.email].password:
        raise HTTPException(status_code=403, detail="Invalid password")
    # If none of these error out, return a success message
    return { "message": "User signed in successfully!" }
