"""
Thomas Horn
Database refactor of mailroom_oo.py
"""

import os
import logging 
from mailroom_db_model import Donor, Donation, SqliteDatabase

logger = logging.getLogger(__name__)
FORMAT = "%(filename)s : %(levelname)s : %(lineno)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class DonorDB:
    """
    Functions used to access the donor database with typical functionality including reporting, creating
    letters, adding donors and or donations, deleting donors, and editing donor info.
    """
    def __init__(self, database):
        """ Parameter must be a SqliteDatabase. """
        self.database = database
    
    



if __name__ == "__main__":
    # Pass database to DonorDB constructor
    db = DonorDB(SqliteDatabase('mailroom_database.db'))