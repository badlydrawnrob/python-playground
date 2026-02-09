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
# 6. Your claims should include at least `iss`uer, `aud`ience, and `exp`iry
# 7. Your website should always use HTTPS (never HTTP)
#
# Never add sensitive data to the JWT payload!
# If you add a token refresh endpoint (YAGNI), be extremely careful.
# Always have a mentor or professional check your code!
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
# > `time.time()` gives us a POSIX timestamp, also known as UNIX time. This
# > represents the number of seconds elapsed since the UNIX epoch.
#
# 1. `time.time()` gives us a POSIX number which you can add to
#     - `60` seconds `*` [whatever you want]
#     - `datetime.timedelta(hours=0, minutes=0, seconds=60)` can also be used
# 2. You can convert POSIX timestamp to human readable time
#     - @ https://www.epochconverter.com/
#     - @ https://www.tech-reader.blog/2025/10/handling-time-zones-in-python-avoiding.html
#     - `datetime.fromtimestamp(POSIX_TIMESTAMP, tz=timezone.utc)`
#     - `datetime.now(timezone.utc)` or `datetime.now(tz=ZoneInfo("UTC"))`
# 3. You can convert POSIX to and from `datetime`
#     - @ https://note.nkmk.me/en/python-unix-time-datetime/
# 4. Remember that people use VPNs which could drastically alter the time
#     - For this reason, consider using a default timezone!
# 5. Use AWARE datetimes and not naive ones (naive datetimes deprecated)
#     - Aware datetimes have a timezone attached. If not they could break the app!
#     - Imagine your users don't live in the same city: a calendar entry gives
#       different results depending on where you live if it's naive.
#     - @ https://tinyurl.com/miguel-utcnow-deprecated
# 6. UTC is the primary time standard for the world to regulate clocks and time
#     - Using a single timezone assures every entry will sync between users
# 7. For arithmetic UTC integers are far less error prone, take up less memory,
#    and are much more efficient than `Iso8601` strings (the values we use for
#    our `json API`, see (8)).
# 8. Elm Lang has an `Iso8601` package and a `toTime` (`Time.Posix`) function
#     - Very handy for regular `String` times and converting to `Hour` etc.
# 9. If you require a timezone to display to a user, convert UTC timestamp
#     - `utc_now.astimezone(ZoneInfo("Asia/Tokyo"))`
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
    """Base64url-encoded string with three parts
    
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
