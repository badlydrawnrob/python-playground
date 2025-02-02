from fastapi import FastAPI
from todo import todo_router

# ------------------------------------------------------------------------------
# A to do app
# ==============================================================================
# See `chapter_02` and `chapter_03` for full instructions.
#
# 1. Run the server: `uvicorn api:app --port 8000 --reload`.
# 2. Run BRUNO (the app) and keep well documented.
#
# Security
# --------
# > Validate and SANITIZE (malicious input)
# > Always authenticate the user.
# > Use a login token and CSRF for forms
# > Don't share secrets online (Github tokens)
#
# Data
# ----
# > Beware: duplicate `:id`, empty list, mutable data, so on.
# > Warn: the user of irriversible changes (`DELETE` all)
#
# Response codes
# --------------
# > `200`, `201`, `404`, `500` are most common
# > @ https://umbraco.com/knowledge-base/http-status-codes/

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello Buddy!" }

app.include_router(todo_router)
