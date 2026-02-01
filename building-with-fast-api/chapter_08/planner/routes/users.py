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
# WISHLIST
# --------
# 1. ⭐️ Figure out how to `/signin` with Elm and CURL
# 2. ⚠️ Check the error status code and create custom one
# 3. Use a `TypedDictionary` for the `/signin` response type?
# 4. Change `username` to `public` UUID for JWT?

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
async def sign_new_user(data: User) -> dict:
    """Register a new user account.
    
    > ⚠️ Do not use in production! This isn't secure enough.
    > Piccolo's `BaseUser` handles password hashing and salting for us.
    
    This route allows new users to sign up. In a production app you'd want
    email verification, captcha, and other security measures to avoid bots
    signing up fake accounts (that's a lot of work!).
    
    Startups can use an invite-only system and manually create users with
    Piccolo's CLI.

    Errors
    ------
    > Possible things that can go wrong ...
    
    1. 🔐 Does not create a secure password (Piccolo checks `< 6` characters)
    2. 📧 Email is not a proper email (Piccolo does not check this)
    3. 📧 Email already exists (sqlite3.IntegrityError)
    4. 👤 Username already exists (sqlite3.IntegrityError)
    5. ❌ Value is `None` for required fields (sqlite3.IntegrityError)
    5. 🛑 Account not approved by admin (`active=False`)
    """
    try:
        new_user = BaseUser.create_user(
            username=data.username,
            email=data.email,
            password=data.password
            active=True #! (4)
        )
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Username or email already exists | {e}"
        )

    return { "message": f"User with {new_user.email} registered!" }


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
    user = await BaseUser.login(data.username, data.password)

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
async def retrieve_user_profile() -> dict:
    """Retrieve user profile and all their events
    
    > #! TO DO: Finish this route properly.
    > Only retrieve events created by the (current) authenticated user.

    This isn't in the book, but think it's a useful (and necessary) addition.
    You're definitely going to allow the user to view and edit their profile!
    """
