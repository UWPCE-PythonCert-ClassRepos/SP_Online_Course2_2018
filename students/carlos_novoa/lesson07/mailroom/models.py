"""
This module defines Donor DB Models
"""
from peewee import *  # noqa F403
database = SqliteDatabase('mailroom.db')  # noqa F403


class BaseModel(Model):  # noqa F403
    class Meta:
        database = database


class Donor(BaseModel):
    """
    This class defines the Donor model
    """
    first_name = CharField(max_length=30)  # noqa F403
    last_name = CharField(max_length=30)  # noqa F403


class Donation(BaseModel):
    """
    This class defines Donations model.
    Using system PK to be able to select
    donations for editing/deleting
    """
    donation = FloatField()  # noqa F403
    donor = ForeignKeyField(Donor, field='last_name', null=False)  # noqa F403
