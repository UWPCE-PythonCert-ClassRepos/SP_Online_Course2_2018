#!/usr/bin/env python3

import logging
from functools import reduce
from create_donor import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('donation.db')

class Donor:

    def __init__(self, name, list_donations):
        self._name = name
        self._list_donations = list_donations
        self._donation_count = len(list_donations)
        self._amount = sum(list_donations)


    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def add(self, donation_amount):
        self._amount +=donation_amount
        self._donation_count += 1
        self._list_donations.append(donation_amount)


    @property
    def donation_count(self):
        return self._donation_count

    @property
    def average(self):
        return self._amount / self._donation_count

    def get_letter_text(self, name, amount):
        msg = []
        msg.append('Dear {},'.format(name))
        msg.append('\n\n\tThank you for your very kind donation of ${:.2f}.'.format(amount))
        msg.append('\n\n\tIt will be put to very good use.')
        msg.append('\n\n\t\t\t\tSincerely,')
        msg.append('\n\t\t\t\t-The Team\n')
        return "".join(msg)

    def __lt__(self, other):
        return self._amount < other._amount

    def __gt__(self, other):
        return self._amount > other._amount

    def __eq__(self, other):
        return self._amount == other._amount

class Donations:

    def __init__(self):
        """collection of donors"""
        self._donors = {}

    def insert_donor(self, donor):
        self._donors[donor.name] = donor

    def add_update(self, donor):
        """ add or update donor"""

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # existing donor
            if donor.name in self._donors.keys():
                d =self._donors[donor.name]
                # update donation amount
                d.add(donor.amount)

                #find existing donor in database
                with database.transaction():
                    existing_donor = Donor_Collection.get(Donor_Collection.person_name == donor._name)

                    existing_donor.total_amount += donor._amount
                    existing_donor.donation_count += 1
                    existing_donor.average = existing_donor.total_amount/existing_donor.donation_count
                    existing_donor.save()
                    new_donation_amount = Donation_Amount.create(
                        donation_amount = donor._amount,
                        from_person = donor._name)
                    new_donation_amount.save()
                    logger.info('Database update successful')
            else:
                # new donor
                self._donors[donor.name] = donor
                #new donor
                with database.transaction():
                    new_donor = Donor_Collection.create(
                        person_name = donor._name,
                        donation_count = donor._donation_count,
                        total_amount = donor._amount)

                    new_donor.save()

                    for amount in donor._list_donations:
                        new_donation_amount = Donation_Amount.create(
                            donation_amount = amount,
                            from_person = donor._name)
                        new_donation_amount.save()

                    logger.info('Database add successful')

        except Exception as e:
            logger.info('failed to add or update')
            logger.info(e)

        finally:
            logger.info('database closes')
            database.close()

    def delete(self, donor_name):
        """ delete a donor from database"""

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            Donation_Amount.delete().where (Donation_Amount.from_person == donor_name).execute()

            aDonor = Donor_Collection.get(Donor_Collection.person_name == donor_name)
            logger.info(f'Trying to delete {aDonor.person_name}')
            aDonor.delete_instance()

        except Exception as e:
            logger.info("Delete failed because record doesn't exist: ")
            logger.error("error", e)

        finally:
            database.close()


    @property
    def donors(self):
        return self._donors

    def generate_report(self):
        """Get data from database and Generate report"""

        report = []
        report.append("--------------------------------------------------------------")
        msg = "{:20} | {:10} | {:5} | {:10}".format('Donor Name', 'Total Given', 'Num Gifts', 'Average Gift')
        report.append(msg)
        report.append("--------------------------------------------------------------")

        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        try:
            query = Donor_Collection.select(Donor_Collection).order_by(Donor_Collection.total_amount.desc())

            for aDonor in query:
                average = aDonor.total_amount / aDonor.donation_count
                a_row = '{:20}  $ {:>10.2f}  {:>10d}  $ {:>11.2f}'.format(aDonor.person_name,
                                                                      aDonor.total_amount,
                                                                      aDonor.donation_count,
                                                                      average)
                report.append(a_row)
        except Exception as e:
            logger.info("Record doesn't exist: ")
            logger.info(e)

        finally:
            database.close()

        return "\n".join(report)