from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token

# ------------------------------------------------------------------------------
# Authenticate
# ==============================================================================
# Contains the authenticate dependency, which will be injected into our routes
# to enforce authenticatiion and authorization. This is the single source of
# truth for retrieving a user for an active session!
#
# Depends
# -------
# > We use Dependency Injection method
#
# This means that a function like `Depends(get_user)` is passed into the path
# of the parent function, and must run (and be satisfied) before the function
# can execute it's body. We use the OAuth2 password flow, which requires the client
# to send a username and password as form data. Once these are satisfied, we can
# create an access token (a signed JWT) which will validate credentials sent to
# the server for further requests (with Bearer header).
#
# A JWT is an encoded string usually containing a dictionary housing:
# 
# 1. A payload
# 2. A signature
# 3. It's algorithm
#
# JWTs are signed using a unique key known only to the server and client, which
# avoids the encoded string being tampered with. The `user` field of the payload
# is only returned if the token is valid, otherwise we return an error.

# Tells the application that a security scheme is present
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")

async def authenticate(token: str = Depends(oauth_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=403,
            detail="Sign in for access"
        )
    
    decoded_token = verify_access_token(token) # check validity of token
    return decoded_token["user"]
