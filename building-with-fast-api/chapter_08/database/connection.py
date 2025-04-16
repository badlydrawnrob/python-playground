from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# ------------------------------------------------------------------------------
# Our DATABASE connection
# ==============================================================================
# From here we set up, connect, and open our SQL database to incoming connections.
# For now I'll let FastApi handle creating the database and tables, but this is
# not necessary (and can be done manually).
#
# Questions
# ---------
# 1. Ideally, set SQLite to `STRICT` mode?
#    - @ https://sqlite.org/stricttables.html
# 2. What is `check_same_thread` and is it safe?
#    - @ https://github.com/fastapi/fastapi/discussions/5199
# 3. VISUALLY explain `create_engine()`, `conn()`, and `get_session()`
#    - `conn()` is only required to create the database and tables
#    - I think `get_session()` opens and closes for each request
#    - This is handy for development purposes, but could remove it in favour
#      of setting up the database schema manually.
# 4. I think `session.refresh(OBJECT)` refreshes the database object, so that
#    we can work with it in it's new state.
#     - @ https://sqlmodel.tiangolo.com/tutorial/update/#refresh-the-object
#
# Security
# --------
# 1. We must use an environment variable to store our secrets
#    - This could include the database connection string, a secret key, our
#      API key, etc. We don't want to hardcode these values, nor have them within
#      our codebase in Github (for security reasons).
#    - @ https://medium.com/@mahimamanik.22/environment-variables-using-pydantic-ff6ccb2b8976

# File location ----------------------------------------------------------------

database_file = "planner.db" # created if does not exist
database_connection_string = f"sqlite:///{database_file}"

# Settings ---------------------------------------------------------------------

connect_args = { "check_same_thread": False }

# Database instance ------------------------------------------------------------
# `echo=True` prints out the SQL commands (for debugging)

engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)

# Create database --------------------------------------------------------------
# Any `table=True` classes will be stored in `.metadata`. Creates database.
# @ https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/

def conn():
    SQLModel.metadata.create_all(engine_url)

# Persist the session ----------------------------------------------------------
# In our application
    
def get_session():
    with Session(engine_url) as session:
        yield session
