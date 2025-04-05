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
# > ⭐ Our `User` routes should be treat like a black box.
# > See `chapter_07` for more details.
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
# So in general your app could be invite-only, and you manually create the user
# accounts on their behalf. Once you've got a bit of cash, you can hire a
# professional do build a solid login system for you!
#
# Wishlist
# --------
# 1. Hashing can be slow. Can it be speeded up?
# 2. We should probably disallow `+test` type email addresses.
#    - Although these are useful for testing.
# 3. Are there better encryption methods than `python-jose`?
#    - This "isn't my job", but I should understand the options.
# 4. The expiry time is currently hard-coded to 1 hour.
#    - Should this be an `.env` variable setting?
#    - We need to write a function to extend the expiry time.
# 5. Change our `User` model to use `UUID` AND an `Int Id`
# 6. Do we need a separate `User` and `UserSign` class?
#    - Otherwise all our `User`s will have `Optional` (`None`) fields.

user_router = APIRouter(
    tags=["User"]  # used for `/redoc` (menu groupings)
)

# Hashing password -------------------------------------------------------------

hash_password = HashPassword()

# Routes -----------------------------------------------------------------------

@user_router.post("/signup")
async def sign_new_user(data: User, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == data.email) # Does user exist?
    user = session.exec(statement).first() # There should be ONE row
    
    if user: # `None` if user doesn't exist
        raise HTTPException(status_code=409, detail="Username already exists")

    # Secure the password
    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password # Replace request body password

    # Finally, add the user to database
    session.add(User(email=data.email, password=data.password))
    session.commit()

    return { "message": f"User with {data.email} registered!" }


@user_router.post("/signin", response_model=TokenResponse) #! What's this?
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
        access_token = create_access_token(db_user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
    # User exists but hashed password isn't working ("403 vs 401 wrong password")
    raise HTTPException(status_code=401, detail="Invalid password")
