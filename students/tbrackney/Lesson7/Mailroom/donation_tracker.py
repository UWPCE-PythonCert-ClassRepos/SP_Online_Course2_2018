"""
File Name: donation_tracker.py
Author: Travis Brackney
Class: Python 201 - Self paced online
Date Created 5/16/2018
Python Version: 3.6.4
"""

import logging
import datetime
from peewee import fn, SqliteDatabase
from donordb_model import Donor, Donation
database = SqliteDatabase('donation_tracker.db')

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Donorlist:
    """
    Instance of a list of donors, implemented as a dictionary.  Implements
    methods used in mailroom5.
    """
    def __init__(self, database):
        """
        Takes open connection to donor database.
        """
        self.database = database
        self._short_template = "Dear {}, thank you for your generous donation of ${:.2f}\n"
        self._long_template = ('Dear {},\n'
                               '\n'
                               '        Thank you for your kind donations totaling ${:.2f}\n'
                               '\n'
                               '        Your gifts will be put to very good use.\n\n'
                               '                            Sincerely\n'
                               '                                -The Team\n'
                               )

    def __contains__(self, val):
        """ Returns if a name is in the list of donors"""
        log.debug('Querying for donor name')
        try:
            self.database.connect()
            result = (Donor
                      .select(Donor.name)
                      .where(Donor.name == val)
                      .get()
                      )
            return val == result.name
        except Exception as e:
            log.debug(e)
            return False
        finally:
            self.database.close()

    def list_donors(self):
        """Returns a list of donors sorted by name"""
        try:
            self.database.connect()
            return [donor.name for donor in Donor.select().order_by(Donor.name)]
        except Exception as e:
            log.debug(e)
            return False
        finally:
            self.database.close()

    def list_by_total(self):
        """Returns a list of donors sorted by total donations"""
        try:
            self.database.connect()
            ord = (Donor
                   .select(Donor.name,
                           fn.SUM(Donation.donation_amount).alias('total_donations'),
                           fn.COUNT(Donation.donation_amount).alias('count'),
                           (fn.AVG(Donation.donation_amount).alias('avg'))
                           )
                   .join(Donation)
                   .group_by(Donor.name)
                   .order_by(fn.SUM(Donation.donation_amount).desc())
                   )
            return tuple([(d.name,
                          d.total_donations,
                          d.count,
                          float(d.avg))
                          for d in ord])
        except Exception as e:
            log.debug(e)
        finally:
            self.database.close()

    def list_donations(self, name):
        """Returns list of donations for a donor"""
        try:
            self.database.connect()
            d_list = (Donation.select()
                      .where(Donation.donor_name == name)
                      .order_by(Donation.donation_date)
                      )
            if d_list.count() > 0:
                return [float(d.donation_amount) for d in d_list]
            else:
                raise ValueError('No Donations Found')
        except Exception as e:
            log.debug(e)
        finally:
            self.database.close()

    def add_donor(self, name):
        """Adds a new donor to the list with a blank donation history"""
        # if name not in self._donor_objects.keys():
        #     self._donor_objects[name] = Donor(name, [])
        # else:
        #     raise ValueError(f"Duplicate name in {type(self)}")
        try:
            self.database.connect()
            with self.database.transaction():
                new_donor = Donor.create(name=name)
                new_donor.save()
        except Exception as e:
            log.info(e)
            raise ValueError(f"Duplicate name in {type(self)}")
        finally:
            self.database.close()

    def add_donation(self, name, amt):
        # self._donor_objects[name].add_donation(amt)
        try:
            self.database.connect()
            if name in self:
                now = datetime.datetime.now()
                try:
                    with database.transaction():
                        nd = Donation.create(donor_name=name,
                                             donation_amount=amt,
                                             donation_date=now.strftime("%Y-%m-%d"))
                        nd.save()
                except Exception as e:
                    log.info('Error adding donation')
                    log.info(e)
            else:
                raise ValueError(f'Donor {name} not in database, please add')
        except Exception as e:
            log.info(e)
        finally:
            self.database.close()

    def send_thankyou(self, name, amt, template='short'):
        """
        Sends thank you note after donation.  Can pass an alternate template
        if desired.
        """
        if template == 'short':
            template = self._short_template
        elif template == 'long':
            template = self._long_template
        return template.format(name, amt)

    def create_report(self, file_out):
        """Prints report of all donors"""
        categories = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']
        spacing = "{:<20} $ {:>10.2f} {:>10}     $ {:>10.2f}\n"
        sorted_tuple = self.list_by_total()
        header = "{:<20}| {:>10} | {:>10} | {:>10}\n"
        file_out.write(header.format(*categories))
        for donor in sorted_tuple:
            file_out.write(spacing.format(donor.name, donor.total, donor.count, donor.average))

    def get_total(self, name):
        """Returns total donations for donor"""
        # return self._donor_objects[name].total
        try:
            self.database.connect()
            if name in self:
                query = Donation.select(Donation.donor_name,
                                        fn.SUM(Donation.donation_amount).alias('total')
                                        ).where(Donation.donor_name == name)
                if query.count():
                    return query.get().total
                else:
                    return 0
            else:
                raise ValueError('No Donor found')
        except Exception as e:
            log.debug(e)
