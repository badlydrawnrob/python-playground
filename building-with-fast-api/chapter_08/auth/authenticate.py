# ------------------------------------------------------------------------------
# Authenticate
# ==============================================================================
# > We've already validated our user exists in the `/signin` endpoint.
# > This module handles authentication for protected routes by checking the JWT.
# 
# Contains the authenticate dependency, which will be injected into our routes
# to enforce authenticatiion and authorization. This is the single source of
# truth for retrieving a user for an active session!
#
# Dependency Injection
# --------------------
# > `Depends(authenticate)` gets run before the endpoint's body code.
# 
# For more on JWTs and security notes, see `jwt_handler`.
#
# We use the Dependency Injection method to use `authenticate()` and check the
# JWT `access_token` is valid, which will include our claims to check which user
# is currently logged in. The JWT must be satisfied as valid or else an error will
# be raised. We've used the OAuth2 password flow, requiring the client to send
# form data `username` and `password`.
# 
# That created the user's `access_token` (a signed JWT) to validate credentials
# (with Bearer header) sent to the server for future endpoint requests.

from auth.jwt_handler import verify_access_token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from piccolo.apps.user.tables import BaseUser


# Tells the application that a security scheme is present
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")

async def authenticate(token: str = Depends(oauth_scheme)) -> int:
    """Authenticate user by verifying JWT access token.
    
    > Returns the payload data if decoded token is valid.
    > Previously returned the `username` (not the `id`)!

    It's debatable about the best way to store user info in the JWT and
    retrieve user details for use in routes: this is one example. You might
    also want to retrieve other details you can use within authenticated
    endpoints, such as `@email` or `is_admin` status.
    """
    if not token:
        raise HTTPException(
            status_code=403,
            detail="Sign in for access"
        )
    
    decoded_token = verify_access_token(token) # check validity of token

    user = await (
        BaseUser.select()
        .where(
            BaseUser.username == decoded_token["sub"] # was `user`
        ).first()
    )

    return user["id"]
