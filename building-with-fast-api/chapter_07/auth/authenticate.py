# ------------------------------------------------------------------------------
# Authenticate
# ==============================================================================
# Contains the authenticate dependency, which will be injected into our routes
# to enforce authenticatiion and authorization.
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
# avoids the encoded string being tampered with.
