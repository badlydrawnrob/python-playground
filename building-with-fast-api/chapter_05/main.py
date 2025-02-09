from fastapi import FastAPI
from routes.users import user_router
import uvicorn

# ------------------------------------------------------------------------------
# A PLANNER app
# ==============================================================================
# See earlier chapters for full instructions.
#
# Notes
# -----
# Anyone from the public can view an event, but only registered users can create,
# or interact with events.

app = FastAPI()

# Register our routers ---------------------------------------------------------
# We're prefixing the `/user`: `/user/signup` and `/user/signin`

app.include_router(user_router, prefix="/user")

# Run our app ------------------------------------------------------------------
# If you try running this as `.run(app, ...)` you'll get an error:
#   "pass the application as an import string to enable 'reload' or 'workers'"
# The book also uses `0.0.0.0` as the host, but `localhost` is more secure.

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
