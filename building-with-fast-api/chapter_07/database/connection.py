from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# ------------------------------------------------------------------------------
# Our DATABASE connection
# ==============================================================================
# From here we set up, connect, and open our SQL database to incoming connections.
#
# Questions
# ---------
# 1. What is `"check_same_thread"`?
# 2. VISUALLY explain `create_engine()`, `conn()`, and `get_session()`
# 3. What does `session.refresh()` do?
#     - It seems to need an object (I'm so out of touch with OOP!)

# File location ----------------------------------------------------------------

database_file = "planner.db" # created if does not exist
database_connection_string = f"sqlite:///{database_file}"

# Settings ---------------------------------------------------------------------

connect_args = { "check_same_thread": False }

# Database instance ------------------------------------------------------------

engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)

# Create database --------------------------------------------------------------
# And any tables we've described in `/models/...`. Our `.metadata` holds all our
# `table=True` classes we created. This should generally be done once, and if
# you're manually migrating or setting up your database tables, it can safely
# be ignored. @ https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/

def conn():
    SQLModel.metadata.create_all(engine_url)

# Persist the session ----------------------------------------------------------
# In our application
    
def get_session():
    with Session(engine_url) as session:
        yield session
