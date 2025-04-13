from peewee import *
from pydantic import BaseModel
from typing import Optional
from datetime import date

# ------------------------------------------------------------------------------
# Testing from Quickstart
# ==============================================================================
# > Run `python3` from `/testing` folder and import this file
#
# @ https://docs.peewee-orm.com/en/latest/peewee/quickstart.html


# PeeWee models ----------------------------------------------------------------

sqlite_db = SqliteDatabase('people.db')

class DataModel(Model):
    class Meta:
        database = sqlite_db

class Person(DataModel):
    name = CharField()
    birthday = DateField()

class Pet(DataModel):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

# Pydantic models --------------------------------------------------------------
    
class Bobby(BaseModel):
    id: Optional[int] = None
    name: str
    birthday: date

class Snake(BaseModel):
    owner: int
    name: str
    animal_type: str
