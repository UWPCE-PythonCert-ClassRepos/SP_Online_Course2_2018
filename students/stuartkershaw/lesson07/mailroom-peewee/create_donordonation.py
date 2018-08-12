#!/usr/bin/env python3

import logging
import datetime
from peewee import (SqliteDatabase, Model, CharField, ForeignKeyField,
                    DateTimeField, DecimalField)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor, which maintains donor name
    """
    donor_name = CharField(primary_key=True, max_length=30)
    donor_created = DateTimeField(default=datetime.datetime.now)


class Donation(BaseModel):
    """
        This class defines Donation, which maintains donation value and
        donor name.
    """
    donation_donor = ForeignKeyField(Donor, null=False)
    donation_amount = DecimalField(max_digits=8, decimal_places=2)
    donation_date = DateTimeField(default=datetime.datetime.now)


database.create_tables([
    Donor,
    Donation
])

database.close()
