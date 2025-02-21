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
# 1. Should SQLite be set to `STRICT` mode?
#    - @ https://sqlite.org/stricttables.html
# 2. What is `check_same_thread` and is it safe?
#    - @ https://github.com/fastapi/fastapi/discussions/5199
# 3. VISUALLY explain `create_engine()`, `conn()`, and `get_session()`
#    - `conn()` is only required to create the database and tables
#    - I think `get_session()` opens and closes for each request
# 4. What does `session.refresh()` do?
#     - It refreshes the object that's been updated, for example
#     - @ https://sqlmodel.tiangolo.com/tutorial/update/#refresh-the-object

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
