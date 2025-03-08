from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import get_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, TokenResponse
from sqlmodel import select

# ------------------------------------------------------------------------------
# Our USERS routes
# ==============================================================================
# ⚠️ Our password is plain text over the wire, but gets hashed on signup. I'm not
# sure if there's a way to hide the password before it's hashed. In production,
# you never want to store the password as plain text.
#
# Notes
# -----
# We're now adding our user directly into the database, so we'll remove the
# `users` variable. We give them an email as their username, and if their
# password checks out we return a bearer token (JWT). We strictly follow the
# OAuth spec using the `OAuth2PasswordRequestForm` and our `/auth` functions.
#
# Wishlist
# --------
# 1. Hashing can be slow. How can it be speeded up?
# 2. What about `+test` type email addresses?
#    - Should these be disallowed?
# 3. Which encryption package is best?
#    - Should I use an alternative method to `python-jose`?

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)

# Hashing password -------------------------------------------------------------
# We're using a `HashPassword` class to hash our passwords.

hash_password = HashPassword()

# JWT --------------------------------------------------------------------------
# Comprises the user ID and an expiry time before encoding into a long string.
# I'm not sure if there's a way to store further information (like auth group)

# Routes -----------------------------------------------------------------------
# Our database users should have a unique ID, which is a number or UUID. We'll
# create this automatically and use our `User.email` to check against on sign-up.
#
# 1. #! I used to be using `UserSign`, which had only the `str` for `email` and
#    `password`. This felt a little fragile, but using the `User` class with an
#    optional `events` field, which can be set to `None` to begin with.
#    - @ ... see the old version here
# 2. @ https://tinyurl.com/fastapi-oauth2-depends and we're now using the user's
#    email as their USERNAME on sign-in. Go figure. See also `README.md` for why
#    `response_model=` is required here (and not a return type).

@user_router.post("/signup")
async def sign_new_user(user: User, session=Depends(get_session)) -> dict:
    # First check if user already exists
    statement = select(User).where(User.email == user.email)
    user = session.exec(statement).first()
    
    if user: # This could be `None` if user doesn't exist
        raise HTTPException(status_code=409, detail="Username already exists")

    # Hash the password (using `user` which is a `UserSign` class)
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password

    # Now add the user with their newly hashed password
    session.add(User(email=user.email, password=user.password)) #! (1)
    session.commit()

    return { "message": f"User with {user.email} registered!" }


@user_router.post("/signin", response_model=TokenResponse) #! (2)
async def sign_in_user(
        user: OAuth2PasswordRequestForm = Depends(),
        session=Depends(get_session)
    ):
    # Does a user already exist?
    statement = select(User).where(User.email == user.username)
    db_user_exist = session.exec(statement).first()

    if db_user_exist is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if hash_password.verify_hash(user.password, db_user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
    # if hashed password doesn't work ... ("403 vs 401 wrong password")
    raise HTTPException(status_code=401, detail="Invalid password")
