# ------------------------------------------------------------------------------
# JWT Token handler
# ==============================================================================
# > Uses the `python-jose` package which helps encode/decode JWT strings
# > @ https://pypi.org/project/python-jose/
# 
# JWTs are signed with a `SECRET` key known only to the sender and the receiver,
# using the `HS256` algorithm which is perfect for when you own the full stack.
# If you don't have control of the client, consider the `RS256` algorithm instead.
#
# 
# JWT
# ---
# > A JWT is an encoded string usually containing a dictionary. For now, ONLY
# > use as authentication (not to save database calls for user info).
#
# 1. A payload (dict containing values to be encoded)
# 2. A signature (key used to sign the payload)
# 3. It's algorithm (most common is HS256)
#
#     @ https://www.jwt.io/ (check your tokens are valid)
#
# A JWT can be encoded/decoded with `base64`. Our signature will NOT decode, as
# that requires the `SECRET` which will be handled on the backend.
#
#
# Security: secrets
# -----------------
# > ⚠️ Never expose `SECRET` key. Keep it safe and refreshed on a regular basis!
#
# JWTs are signed using a unique key known only to the server and client, which
# avoids the encoded string being tampered with. If someone gets a hold of it,
# they could torpedo your app. KISKIS.
#
#     @ https://en.wikipedia.org/wiki/Key_size (128-256 bits)
# 
# Double check all security settings with an expert! To generate a random 256
# bit (32 char) key in terminal, you can use `openssl`:
#
# ```
# openssl rand -hex 32
# ```
#
# Security: best practices
# ------------------------
# > @ https://datatracker.ietf.org/doc/html/rfc7519
# > @ https://curity.io/resources/learn/jwt-best-practices/
# > @ https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims
# > @ https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-structure
#
# 1. Your JWT should expire in a 30mins—2hrs (not days)
# 2. Your JWT should include minimal non-identifying info (username/userid)
# 3. Your `SECRET` key should be the correct length (256 bits / 32 chars)
# 4. Your `SECRET` should never be exposed! Keep it secure and safe!
# 5. Your `SECRET` should be refreshed often (every couple of weeks or so).
# 6. Your claims should include at least `iss`uer, `aud`ience, and `exp`iry`
# 7. Your website should always use HTTPS (never HTTP)
#
# Never add sensitive data to the JWT payload!
# If you add a token refresh endpoint (YAGNI), be extremely careful.
# Always have a mentor or professional check your code!
#
# Security: calling the API
# -------------------------
# > @ https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/
#
# You may need to use a `client_id` and `client_secret` to call your API. I think
# if your API and client are on the same domain, you can leave out the `client_secret`,
# and just use the `client_id` as well as HTTP headers. However, using a client
# secret is more secure!
#
# Security: expiry
# ----------------
# > Your JWT should expire in a couple of hours (not days)
#
# Use the `Time` module in Elm with the same method that `"expiry"` is encoded.
# You can then notify the user "Login expires in ___ minutes, you'll have to
# login again".
#
#
# User details
# ------------
# > If you require user info, use the `authenticate()` function or ping a
# > `/profile` endpoint like Auth0 as it's more secure.
#
# Once you've verified the JWT, you can use the `"user"` value to lookup user,
# and get their details from the database. This might be their preferences, the
# user type (admin/regular), etc.
#
#
# Understanding Time
# ------------------
# > See `/words/time.md` for a detailed explanation of time in programming.
#
# TL;DR: AWARE datetimes with a timezone must be used so JWTs can be verified
# at their correct expiry time. UTC is used here as the default timezone.
#
#
# WISHLIST
# --------
# 1. Add the `iss`uer and `aud`ience (and verify in the function)
# 2. Check the `iss` and `aud` fields when verifying token

from datetime import datetime, timezone
from fastapi import HTTPException
from planner.piccolo_app import SECRET
from jose import jwt, JWTError
import time


def create_access_token(username: str) -> str:
    """Base64 url-encoded string with three parts
    
    > Encodes user info securely.
    > @ https://datatracker.ietf.org/doc/html/rfc7519
    
    1. JOSE header: metadata about type of token
    2. JWS payload: set of claims about user and permissions
    3. JWS signature: access token signed with SECRET key
    """
    payload = {
        # "iss": "https://stringoruri.com",
        # "aud": "https://stringoruri.com",
        "sub": username, # Was called `user` (must be a string)
        "exp": time.time() + 3600 # 60sec * 60min = 1 hour
    }
    
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    """Decode JWT and verify it's valid.
    
    Currently only checks:
    
    1. Was the token supplied?
    2. Expiry with a UTC timestamp.
    """
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        expire = data.get("exp")

        if expire is None:
            raise HTTPException(
                status_code=400, # bad request
                detail="No access token supplied"
            )

        if datetime.now(tz=timezone.utc) > datetime.fromtimestamp(expire, tz=timezone.utc):
            raise HTTPException(
                status_code=403, # forbidden
                detail="Token expired!"
            )
        
        return data

    except JWTError: # @ https://github.com/mpdavis/python-jose/issues/25
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )
