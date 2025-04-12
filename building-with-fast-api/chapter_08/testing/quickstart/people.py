from peewee import *

# ------------------------------------------------------------------------------
# Testing from Quickstart
# ==============================================================================
# > Run `python3` from `/testing` folder and import this file
#
# @ https://docs.peewee-orm.com/en/latest/peewee/quickstart.html

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
