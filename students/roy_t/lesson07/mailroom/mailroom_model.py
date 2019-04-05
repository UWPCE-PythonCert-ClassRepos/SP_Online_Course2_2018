#!/usr/bin/env python3


import peewee
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Donor:
    """
    Class to build/store donor information
    """

    def __init__(self, first_name, last_name, donations=[]):
        """Create a donor object with basic information."""
        self.name = (first_name, last_name)
        self.donations = donations

    def add_donation(self, amount):
        """Add a donation to a Donor's donation list"""
        self.donations.append(amount)

    def get_donations(self):
        """Return all donations for a donor."""
        return self.donations

    def get_key(self):
        """Use the donor's name for a key. To be used in the database."""
        return self.name

    def get_name(self):
        """Get first and last name of donor."""
        return '{} {}'.format(*self.name)

    def get_name_tuple(self):
        """Return a tuple of the donor's first and last name."""
        return self.name


donations = peewee.SqliteDatabase("mailroom_donors.db")


class BaseModel(peewee.Model):
    """Base model to be used creating the database."""
    class Meta:
        database = donations


class DonorData(BaseModel):
    """Donor Table"""
    donor_name = peewee.CharField(unique=True)
    last_name_index = peewee.IntegerField()

class Donations(BaseModel):
    """Donations table"""
    amount = peewee.IntegerField()
    donated_by = peewee.ForeignKeyField(DonorData, related_name='donations')


class DonorCollection:
    """Collection of donors and donations."""

    def __init__(self):
        """Initialize a collection to save donor objects"""
        DonorData.create_table()
        logger.info('Donor table created.')
        Donations.create_table()
        logger.info('Donations table created.')

    def get_donors(self):
        """Return all donor information in the database."""
        all_donors = DonorData.select()
        logger.info('Iterating over donors.')
        for d in all_donors:
            all_donations = list()
            for donation in d.donations:
                all_donations.append(donation.amount)

            first_name = d.donor_name[:d.last_name_index]
            last_name = d.donor_name[d.last_name_index:]
            yield Donor(first_name, last_name, all_donations)

    def get_donor(self, first_name, last_name):
        """Query the database and return the donor's first and last name."""
        name = first_name + last_name
        index = len(first_name)
        donors = DonorData.select().where(DonorData.donor_name == name)

        if len(donors) == 0:
            donor = DonorData.create(
                donor_name=name,
                last_name_index=index
            )
        else:
            donor = donors.get()
        return donor

    def add_donation(self, first_name, last_name, amount):
        """Add a new donation to the database."""
        donor = self.get_donor(first_name, last_name)
        Donations.create(amount=amount, donated_by=donor)

    def delete_donor(self, first_name, last_name):
        """Delete a donor from the database."""
        donor = self.get_donor(first_name, last_name)
        for donation in donor.donations:
            donation.delete_instance()
        donor.delete_instance()

    def get_donations(self, first_name, last_name):
        """Get all donations for a donor from the database."""
        donor = self.get_donor(first_name, last_name)
        donations_list = list()
        for donation in donor.donations:
            donations_list.append(donation.amount)
        return donations_list

    def delete_donation(self, first_name, last_name, delete_num):
        """Delete a donation for a specific donor."""
        donor = self.get_donor(first_name, last_name)
        donations = donor.donations
        donations[delete_num].delete_instance()

    def modify_donation(self, first_name, last_name, change_num, new_amount):
        """Modify an existing donation amount."""
        donor = self.get_donor(first_name, last_name)
        donations = donor.donations
        donations[change_num].amount = new_amount
        donations[change_num].save()

    def modify_donor_name(self, first_name, last_name, new_first, new_last):
        """Modify an existing donor name in the database."""
        logger.info(f'Modifying donor: {first_name} {last_name}')
        new_name = new_first + new_last
        new_index = len(new_first)
        donor = self.get_donor(first_name, last_name)
        donor.donor_name = new_name
        donor.last_name_index = new_index
        donor.save()
        logger.info('Donor modified successfully.')
