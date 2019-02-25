"""custom base model for ORM in mailroom"""

from . config import database
from peewee import *

class BaseModel(Model):
    class Meta:
        database = database

