"""
Module for performing donor database actions
"""

import logging
from peewee import *  # noqa F403
from models import *  # noqa F403
from helpers import *  # noqa F403

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom.db')  # noqa F403


class Queries:
    """ Defines Queries class for interacting with DB """

    # ::: DONORS :::::::::::::::::::::::::::::::::::::::::: #

    @staticmethod
    def get_donor_by_last(last_name):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            d = Donor.get(Donor.last_name == last_name)  # noqa F403
            # logger.info(f"Donor found: {last_name}")
            return d
        except Exception as e:
            # logger.info(f"Donor not found.")
            return False
        finally:
            database.close()

    @staticmethod
    def get_donor_by_id(donor_id):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            d = Donor.get(Donor.id == donor_id)  # noqa F403
            # logger.info(f"Donor found: {donor_id}")
            return d
        except Exception as e:
            # logger.info(f"Donor not found.")
            return False
        finally:
            database.close()

    @staticmethod
    def get_donors():
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            dl = list(Donor.select().execute())  # noqa F403
            # logger.info(f"Donors found.")
            return dl
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def insert_donor(donor):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            Donor.insert(  # noqa F403
                first_name=donor.first_name,
                last_name=donor.last_name).execute()
            # logger.info(f"Inserted: {donor.first_name} {donor.last_name}")
            return True
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def update_donor(donor_id, first_name, last_name):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            person = (Donor  # noqa F403
                    .update(first_name=first_name, last_name=last_name)
                    .where(Donor.id == donor_id)  # noqa F403
                    .execute())
            # logger.info(f'Updated {first_name} {last_name}')
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    # ::: DONATIONS :::::::::::::::::::::::::::::::::::::::::: #

    @staticmethod
    def insert_donation(donor_id, donation):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # lookup
            row = Donor.get_by_id(donor_id)  # noqa F403
            last_name = row.last_name
            # donation table
            Donation.insert(donation=donation, donor=last_name).execute()  # noqa F403
            # logger.info(f"Inserted: {last_name}, {donation}")
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def delete_donation(donation_id):
        """ deletes one donation """
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donation table
            Donation.delete().where(Donation.id == donation_id).execute()  # noqa F403
            # logger.info(f'Deleted id: {donation_id}')
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def delete_donations(donor_id):
        """ deletes all donations for given donor """
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # lookup
            row = Donor.get_by_id(donor_id)  # noqa F403
            last_name = row.last_name
            # donations table
            Donation.delete().where(Donation.donor == last_name).execute()  # noqa F403
            # logger.info(f'Deleted: {last_name}')
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    # ::: DONORS AND DONATIONS :::::::::::::::::::::::::::::::::::::::::: #
    def get_donor_single_summary(self, donor_id):
        try:
            """
            Compiles a list for printing a single donor summary
            Called methods establish DB connection
            """
            nl = list()
            d = Donor.get_by_id(donor_id)  # noqa F403
            if d:
                first = d.first_name
                last = d.last_name
                total = self.donations_total(d.id) if self.donations_total(d.id) else 0
                count = self.donations_count(d.id) if self.donations_count(d.id) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([first, last, total, count, average])

            # logger.info('Donor found: {donor_id}')
            return nl

        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    def get_donor_multiple_summary(self):
        try:
            """
            Compiles a list for printing multiple donor summaries
            Called methods establish DB connection
            """
            nl = list()
            donors = self.get_donors()
            for d in donors:
                first = d.first_name
                last = d.last_name
                total = self.donations_total(d.id) if self.donations_total(d.id) else 0
                count = self.donations_count(d.id) if self.donations_count(d.id) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([first, last, total, count, average])
            # logger.info('Donors/donations found.')
            return nl

        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    def delete_donor_donations(self, donor_id):
        """ deletes donor and all donations associated with donor """
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # lookup
            row = Donor.get_by_id(donor_id)  # noqa F403
            last_name = row.last_name
            # donations table
            self.delete_donations(donor_id)
            # donor table
            row.delete().where(Donor.last_name == last_name).execute()  # noqa F403
            # logger.info(f'Deleted: {last_name}')
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def insert_donor_donation(donor, donation):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            Donor.insert(  # noqa F403
                first_name=donor.first_name,
                last_name=donor.last_name).execute()
            # donation table
            Donation.insert(donation=donation, donor=donor.last_name).execute()  # noqa F403
            # logger.info("Inserted: {}, {}, {}".format(
            #             donor.first_name,
            #             donor.last_name,
            #             donation))
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def donations_total(donor_id):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            row = Donor.get_by_id(donor_id)  # noqa F403
            last_name = row.last_name
            query = (Donation # noqa F403
                .select(fn.SUM(Donation.donation).alias('total')) # noqa F403
                .where(Donation.donor == last_name) # noqa F403
                .execute()) # noqa F403
            # logger.info(f"Total: id-{donor_id}, {query[0].total}")
            return query[0].total # noqa F403
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    @staticmethod
    def donations_count(donor_id):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            row = Donor.get_by_id(donor_id)  # noqa F403
            last_name = row.last_name
            query = (Donation # noqa F403
                .select(fn.COUNT(Donation.donation).alias('count')) # noqa F403
                .where(Donation.donor == last_name) # noqa F403
                .execute()) # noqa F403

            # logger.info(f"Count: id-{donor_id}, {query[0].count}")
            return query[0].count
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()

    def donations_average(self, donor_id):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            total = self.donations_total(d.id) if self.donations_total(d.id) else 0
            count = self.donations_count(d.id) if self.donations_count(d.id) else 0
            average = 0
            if total > 0 and count > 0:
                average = total / count
            # logger.info(f"Average: id-{donor_id}, {average}")
            return average
        except Exception as e:
            logger.info(e)
            return False
        finally:
            database.close()
