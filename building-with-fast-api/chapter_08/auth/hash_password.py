# ------------------------------------------------------------------------------
# Password hashing
# ==============================================================================
# This file will contain the functions that will be used to encrypt the password
# of a user during sign-up and compare passwords during sign-in.
#
# `uv add "passlib[bcrypt]"`
#
# Here we're taking a `String` password and hashing it. We do the same in
# reverse when we want to compare the password during sign-in. Our `verify_hash`
# function compares the password with the hash and returns a boolean value.

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)
    
    def verify_hash(self, password: str, hash: str):
        return pwd_context.verify(password, hash)
