import time
from datetime import datetime
from fastapi import HTTPException
from jose import jwt, JWTError
from database.settings import Settings

# ------------------------------------------------------------------------------
# JWT Token handler
# ==============================================================================
# Once again the book isn't specific over which package to install. I'm pretty
# sure `python-jose` is the one, but there's a `jose` package also. Contains
# functions to encode and decode the JWT strings. JWTs are signed with
# a secret key known only to the sender and the reciever, but it might be visible
# to outside users if using a javascript frontend.
#
# A JWT is an encoded string usually containing a dictionary housing:
#
# 1. A payload (dict containing values to be encoded)
# 2. A signature (key used to sign the payload)
# 3. It's algorithm (most common is HS256 algorithm)
#
# @ https://pypi.org/project/python-jose/
# @ #! https://tinyurl.com/miguel-utcnow-deprecated
#
# ⭐ Decoders
# -----------
# > Our `payload` is simply `base64` encoded ...
# > Our token, however won't decode (it needs the `SECRET_KEY`)
#
# Which means we can decode it with base64 too! For the `expires` value, we need
# to use the `Time` module in Elm (with same method as it's encoded).
#
#
# Wishlist
# --------
# > We need a public id that's short enough for a URL ...
#
# 1. But we could use a `token.uuid` and `token.shortuuid` and serve both for
#    our public/private IDs (encode/decode with `base57`)

settings = Settings() # Get the secret key

def create_access_token(user: str) -> str:
    payload = {
        "user": user, # email address
        "expires": time.time() + 3600 # Expires in 1 hour
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        # No token was supplied?
        if expire is None:
            raise HTTPException(
                status_code=400, # bad request
                detail="No access token supplied"
            )

        # Token has expired?
        if datetime.utcnow() > datetime.utcfromtimestamp(expire): #! see link
            raise HTTPException(
                status_code=403, # forbidden
                detail="Token expired!"
            )
        
        return data

    except JWTError: # @ https://github.com/mpdavis/python-jose/issues/25
        raise HTTPException(
            status_code=400, # bad request
            detail="Invalid token"
        )
