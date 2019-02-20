
import logging
from peewee import *
from ap_model import *
from datetime import datetime, date, timedelta
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('./maildonor.db', pragmas={'foreign_keys': 1})

def count_donors():
    """calculates nr of donors in database"""
    try:
        database.connect()
        a=Donors.select().count()
        database.close()
        return a
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def add_donor(donor):
    """
        Populates donors table in database
    """
    try:
        database.connect()                   #
        if ' ' in donor:
            first, last = donor.split(' ')
        else:
            first = ''
            last = donor
        donor_s=(donor, last, first)
        with database.transaction():
            new_donor = Donors.create(
                donor_name =donor_s[0],
                lastname=donor_s[1],
                firsttname=donor_s[2])
            new_donor.save()
        logger.info(f'{new_donor.donor_name} added to Donors table')
    except Exception as e:
        logger.info(f'Error creating = {donor_s[0]}')
        logger.info(e)
    finally:
        database.close()

def add_donation(donor, amount, date=date.today()):
    """Populates donations table in database"""
    try:
        database.connect()
        d=date - timedelta(days=random.randint(1, 100))
        with database.transaction():
            new_donation = Donations.create(
                donor_key =donor,
                amount=amount,
                date=d)
            new_donation.save()
            logger.info(f'{new_donation.donor_key} {new_donation.amount} '
                    +f'{new_donation.date}  added to Donations table')
    except Exception as e:
        logger.info(f'Error creating = {donor} {amount}, {date}')
        logger.info(e)
    finally:
        database.close()

def donor_totals():
    """ Calls DB to calculate count of donations for all donors"""
    try:
        database.connect()
        query = (Donors.select(Donors.donor_name,
                    fn.sum(Donations.amount).alias('donation_total'),
                    fn.COUNT(Donations.amount).alias('num_donations'))
                    .join(Donations, JOIN.LEFT_OUTER)
                    .where(Donations.amount > 0)
                    .group_by(Donors.donor_name)
                    .order_by(fn.sum(Donations.amount).desc()))
        ls=[(item.donor_name, item.donation_total, item.num_donations,
            item.donation_total/item.num_donations) for item in query.objects()]
        return ls
    except Exception as e:
        logger.info(f'Error getting list of donors')
        logger.info(e)
    finally:
        database.close()

def donors_list():
    """generate donors list"""
    try:
        database.connect()
        query=Donors.select()
        ls=[donor.donor_name for donor in query]
        return ls
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def donor_most_recent_donation():
    """Gets the record for each donor for the most recent date"""
    try:
        database.connect()
        query_date = (Donations.select(Donations.donor_key.alias('Donor_name'),
                            Donations.amount.alias('last_donation'),
                            Donations.date.alias('donation_date'))
                            .group_by(Donations.donor_key))

        ls=[(item.Donor_name, item.last_donation, item.donation_date)
                for item in query_date.objects()]
        return ls
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def list_of_donations():
    """Gets a full list of donations from the database"""
    try:
        database.connect()
        query = (Donors
         .select(Donors, Donations)
         .join(Donations, JOIN.LEFT_OUTER))
        ls=[(item.donor_name, item.amount, item.date, item.firstname,
                        item.lastname) for item in query.objects()]
        return ls
    except Exception as e:
        logger.info(f'Error getting all donations and for all')
        logger.info(e)

    finally:
        database.close()

def update_donation(donor="", old_amount=0, new_amount=0):
    """
    Changes a donation record in the donations table (can be used to update date, time , or donor of this record)
    """
    try:
        database.connect()
        with database.transaction():
            donation_search = Donations.get((Donations.amount == old_amount) &
                (Donations.donor_key==donor))
            donation_search.amount = new_amount
            donation_search.save()
            logger.info(f'Updated {donor} donation from {old_amount} to {new_amount}')
    except Exception as e:
        logger.info('Error updating {} donation in database'.format(donor))
        logger.info(e)
    finally:
        database.close()

def donors_dict(lst=list_of_donations()):
    """ transform the database in a dictionary"""
    donors={}
    for x in lst:
        donors.setdefault(x[0],[]).append(x[1])
    return donors

def delete_donor(donor=""):
    try:
        database.connect()
        with database.transaction():
            adonor = Donors.get(Donors.donor_name == donor)
            adonor.delete_instance()
            logger.info(f'Donor {adonor} deleted')
    except Exception as e:
        logger.info(f'Error deleting donor; Delete all donations and try again')
    finally:
        database.close()

def delete_donation(donor="", amount=0):
    try:
        database.connect()
        with database.transaction():
            adonation = Donations.get((Donations.amount == amount) &
                                      (Donations.donor_key==donor))
            adonation.delete_instance()
            logger.info(f'Donation {amount} for donor {donor} deleted')
    except Exception as e:
        logger.info(f'Error deleting donation')
        logger.info(e)
    finally:
        database.close()


#if __name__ == '__main__':
    #add_donor("Donor AX")
    #add_donation('Donor AX',1000)
    #print(donors_list())
    #print(donor_most_recent_donation())
    #print(list_donor_donations("Donor A"))

    #print ()
    #print (count_donors())
    #print (list_of_donations())
    #print (donor_totals())
    #update_donation('Donor AX', 1000, 5000)
#    print (donors_dict())
    #delete_donor('Donor E')
    #print(donors_list())
    #delete_donation("Donor XX", 2000)
    #print (donor_totals())
    #print (donors_dict())
#    pass
