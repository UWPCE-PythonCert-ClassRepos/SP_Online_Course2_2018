"""custom base model for ORM in mailroom"""

from peewee import *

database_name = 'mailroom.db'
database = SqliteDatabase(database_name)

class BaseModel(Model):
    class Meta:
        database = database

