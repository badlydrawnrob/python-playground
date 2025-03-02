# ------------------------------------------------------------------------------
# JWT Token handler
# ==============================================================================
# Contains functions to encode and decode the JWT strings. JWTs are signed with
# a secret key known only to the sender and the reciever, but it might be visible
# to outside users if using a javascript frontend.
#
# A JWT is an encoded string usually containing a dictionary housing:
#
# 1. A payload
# 2. A signature
# 3. It's algorithm
