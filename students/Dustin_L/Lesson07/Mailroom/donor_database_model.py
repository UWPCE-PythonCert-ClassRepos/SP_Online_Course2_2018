#!/usr/bin/env python3
"""Peewee Database Model Definition"""
from functools import partial
import logging
import peewee as pw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = pw.SqliteDatabase('donor_db.db')
MoneyField = partial(pw.DecimalField, decimal_places=2)


class BaseModel(pw.Model):
    """This class defines the base class for all Peewee data tables"""
    class Meta:
        """Meta class required for Peewee"""
        database = database


class Donor(BaseModel):
    """This class defines individual donors."""
    name = pw.CharField(primary_key=True, max_length=40)
    total_donations = MoneyField()
    ave_donations = MoneyField()


class Donation(BaseModel):
    """This class defines the donations made by all donors."""
    donor_name = pw.ForeignKeyField(Donor, backref='donations')
    amount = MoneyField()


def main():
    """Main function for populating the database"""
    donors = [('Toni Morrison', [1000, 5000, 100]),
              ('Mike McHargue', [12000, 5000, 2500]),
              ("Flannery O'Connor", [38734, 6273, 67520]),
              ('Angelina Davis', [74846, 38470, 7570, 50]),
              ('Bell Hooks', [634547, 47498, 474729, 4567])]

    with database as db:
        logger.info('Adding tables to database')
        db.execute_sql('PRAGMA foreign_keys = ON;')
        db.create_tables([Donor, Donation])

        logger.info('Adding donors to database')
        for donor, donations in donors:
            Donor.create(name=donor,
                         total_donations=sum(donations),
                         ave_donations=sum(donations) / len(donations))

        logger.info('Adding donations to database')
        for donor, donations in donors:
            for donation in donations:
                Donation.create(donor_name=donor,
                                amount=donation)


if __name__ == '__main__':
    main()
