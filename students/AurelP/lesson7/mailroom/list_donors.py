import random
import logging
from datetime import datetime, date, timedelta
from peewee import *
from ap_model import *
##from ap_functions import *
#from ap_populate import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('./maildonor.db', pragmas={'foreign_keys': 1})

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

def donors_dict(lst=list_of_donations()):
    """ transform the database in a dictionary"""
    donors={}
    for x in lst:
        donors.setdefault(x[0],[]).append(x[1])
    return donors

if __name__ == '__main__':
    d=donors_dict()
    print ('\nCurrent Donor list:\n')
    for key, value in d.items():
        print ('Donor:', key ,'\n  donations:', value,'\n')
