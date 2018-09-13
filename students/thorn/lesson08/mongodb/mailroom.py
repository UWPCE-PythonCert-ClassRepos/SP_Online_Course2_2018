"""
Main classes of the mailroom.
"""

import login_database
import utilities
import pymongo

log = utilities.configure_logger('default', '../logs/mongo.log')

class Mailroom:
    """ 
    Features:
      - Add
      - Update
      - Delete
      - Show specific donor info
      - Show all donor info
    """

    def __init__()