# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# > We can treat our user routes as a "black box". Shallow learning is OK here.
# > See Piccolo docs for more information, as well as `chapter_07`.
# 
# Authentication is difficult, so we give responsibility to Piccolo. It takes quite
# a bit of learning to understand how authentication systems work, so you might
# want to let a professional handle this for you. All you need to understand is
# that `Depends(authenticate)` checks a user exists and logs them in.
# 
#     @ https://tinyurl.com/fastapi-oauth2-depends
#
# Using Piccolo saves us a ton of hassle (compared to other ORMs) by generating
# our user account which we can add to for a profile endpoint. See the `.schema`
# for `piccolo_user`.
#
#
# Invite only
# -----------
# > The easy route is to manually create users.
# > JWT Bearer tokens can then be used in the request header.
#
# - Our `/signup` route isn't fully secure!
# - Be wary of XXS attacks if you allow open sign-ups.
# - Email verification is a must for production apps.
#
# A common thing for startups is to have an "invite only" process, then you can
# use `piccolo user create` and `BaseUser.login()`. A fully fledged authentication
# system, could use Piccolo's auth API (or roll your own).
#
#
# Data validation
# ---------------
# > Piccolo will handle `BaseUser` stuff automatically ...
# 
# But you'll still need a Pydantic type for the API layer.
#
#
# Alternative authentication methods
# ----------------------------------
# @ https://piccolo-orm.readthedocs.io/en/latest/piccolo/authentication/index.html
# @ https://piccolo-api.readthedocs.io/en/latest/session_auth/index.html
#
#
# ------------------------------------------------------------------------------
# WISHLIST
# ------------------------------------------------------------------------------
# 1. 👩‍🦳 Fix the `/me` endpoint to split `User` from `List[Event]`
# 2. ⭐️ Figure out how to `/signin` with Elm and CURL
# 3. ⚠️ Check the error status code and create custom one
# 4. Use a `TypedDictionary` for the `/signin` response type?
# 5. Change `username` to `public` UUID for JWT?

from auth.authenticate import authenticate
from auth.jwt_handler import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from piccolo.apps.user.tables import BaseUser
import planner.tables as data
import planner.models.events as api
from planner.models.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)


# ------------------------------------------------------------------------------
# Write routes
# ==============================================================================
# Convert from a Pydantic API type -> Pydantic DATA type

@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    """Register a new user account.
    
    > ⚠️ Not fully secure ... do not use in production!
    > Piccolo's `BaseUser` handles password hashing and salting for us.
    
    In a production app you'd want email verification, captcha, and other security
    measures to avoid bots signing up fake accounts (that's a lot of work!). If
    your app is a startup, you could use an invite-only system and manually create
    users with Piccolo's CLI.

    Exceptions
    ----------
    > This is the only endpoint we're "properly" dealing with errors!

    I do not like `try/except` blocks much, and there's no particularly graceful
    way to handle errors: Python's `match` is NOT the same as `case` in Elm. I'd
    possibly rather deal with logging errors than pepper these everywhere.

    Errors
    ------
    > Possible things that can go wrong ...
    
    1. 🔐 Does not create a secure password (Piccolo checks `< 6` characters)
    2. <s>📧 Email is not a proper email</s> (Only Pydantic handles this, not Piccolo)
    3. <s>📧 Email already exists (sqlite3.IntegrityError)</s> (handled by SQLite)
    4. <s>👤 Username already exists (sqlite3.IntegrityError)</s> (handled by SQLite)
    5. <s>❌ Value is `None` for required fields</s> (handled by Pydantic/SQlite)
    6. ❌ Response value giving away sensitive info (avoid this!)
    7. 🛑 Account not approved by admin (change to `active=False` if needed)
    """
    try:
        new_user = await BaseUser.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            active=True #! (4)
        )
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Username or email already exists | {e}"
        )

    return { "message": f"User {new_user.username} with email {new_user.email} registered!" }


# ------------------------------------------------------------------------------
# Read routes
# ==============================================================================
# See `/auth` folder for authentication helpers

@user_router.post("/signin", response_model=TokenResponse)
async def sign_in_user(data: OAuth2PasswordRequestForm = Depends()):
    """Checks if a user exists and returns a JWT

    > `OAuth` specifically requests `username` and `password` data.
    > @ https://docs.usebruno.com/auth/oauth2-2.0/password-credentials
    > @ https://blog.usebruno.com/oauth-2.0-secure-api-access-using-bruno
    
    Types are a bit of a problem at the moment with Oauth.
    """
    user = await BaseUser.login(
        username=data.username,
        password=data.password
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User doesn't exist or password is incorrect" #! 403? 401?
        )

    access_token = create_access_token(data.username)

    return {
        "access_token": access_token, # (5)
        "token_type": "Bearer"
    }


@user_router.get("/me")
async def retrieve_user_profile(user: int = Depends(authenticate)):
    """Retrieve user profile and all their events
    
    > ⚠️ Only current user events should be returned (no sensitive details)

    This isn't in the book, but it's a useful (and necessary) addition.
    You're definitely going to allow the user to view and edit their profile!
    If you need to _edit_ the user details, consider looking around at how
    other apps do it (Google has edit password alone on it's own page).
    
    Joins
    -----
    > Piccolo full joins behind the scenes, so you can access columns.

    Unfortunately we've got a repeating user profile in each event. Ideally,
    we'd want to have a dictionary of `User` and _then_ the `List[Event]`. To do
    that we could (a) manipulate the current data, (b) use raw SQL, (c) create
    our own custom `join_on`, or (d) grab the `User` first, then the `List[Event]`.
    """
    return await (
        data.Event.select(
            data.Event.creator.username,
            data.Event.all_columns()
        ).where(data.Event.creator == user)
    )
