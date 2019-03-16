"""donor class controlling donor behavior"""

from peewee import CharField
from . BaseModel import BaseModel


class Donor(BaseModel):
    """donor giving to organization"""
    donor_name = CharField(primary_key=True, max_length=55)
    email = CharField(max_length=55, null=True)
