from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
import uvicorn

# ------------------------------------------------------------------------------
# A PLANNER app
# ==============================================================================
# See earlier chapters for full instructions on FastApi etc. In this chapter
# we're learning how to implement routes and app architecture. The rest of our
# code we've seen before!
#
# Notes
# -----
# Currently this doesn't specifiy that ONLY signed in users can create and update
# events, as there's no auth involved. We'll need to add those checks in.

app = FastAPI()

# Register our routers ---------------------------------------------------------
# We're prefixing the `/user`: `/user/signup` and `/user/signin`

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# Run our app ------------------------------------------------------------------
# If you try running this as `.run(app, ...)` you'll get an error:
#   "pass the application as an import string to enable 'reload' or 'workers'"
# The book also uses `0.0.0.0` as the host, but `localhost` is more secure.

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
