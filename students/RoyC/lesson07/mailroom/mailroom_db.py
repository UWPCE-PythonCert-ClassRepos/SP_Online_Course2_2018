#!/usr/bin/env python3
# Lesson 7, Mailroom database model

from peewee import *

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class MailroomDbModel(Model):
    class Meta:
        database = database

class SingleDonor(MailroomDbModel):
    """
    Table definition for a single donor
    """
    name = CharField(primary_key = True, max_length = 30, unique = True, null = False)
    total_donations = FloatField()
    avg_donation = FloatField()

class Donation(MailroomDbModel):
    """
    Table definition for a single donation
    """
    amount = FloatField()
    donor = ForeignKeyField(SingleDonor, related_name='was donated by', null = False)

# flag to indicate DB has been created so it is only done once
db_created = database.table_exists('donation')

database.create_tables([
        SingleDonor,
        Donation
    ])

def populate_db(populate):
    """
    Initially populate the database
    """
    # define a starting set of donors
    donors_array = [
        ("Ned Flanders", [1200.25, 850.35]),
        ("Martin Prince",[12.22, 19.56]),
        ("Edna Krabappel",[55.43, 118.67, 75.23]),
        ("Homer Simpson",[253.64, 772.50, 99.99]),
        ("Moe Szylak",[54.23])
    ]

    # populate our database 
    if populate:
        for donor in donors_array:
            with database.transaction():
                total_donations = sum(donor[1])
                avg_donation = total_donations / len(donor[1])
                new_donor = SingleDonor.create(name = donor[0], total_donations = total_donations, avg_donation = avg_donation)
                new_donor.save()
                for donation in donor[1]:
                    new_donation = Donation.create(donor = donor[0], amount = donation)
                    new_donation.save()

populate_db(not db_created)

database.close()