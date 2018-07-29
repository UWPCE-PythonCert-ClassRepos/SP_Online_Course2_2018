#!/usr/bin/env python3
"""This module contains all of the database specific operations for the
    Peewee Database Mail Room
"""
import logging
from donor_dict import DonorDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    donor_db = DonorDict()
    donor_data = [{donor_db.name_key: 'Toni Morrison', donor_db.donations_key: [1000, 5000, 100]},
                  {donor_db.name_key: 'Mike McHargue', donor_db.donations_key: [12000, 5000, 2500]},
                  {donor_db.name_key: "Flannery O'Connor", donor_db.donations_key: [38734, 6273, 67520]},
                  {donor_db.name_key: 'Angelina Davis', donor_db.donations_key: [74846, 38470, 7570, 50]},
                  {donor_db.name_key: 'Bell Hooks', donor_db.donations_key: [634547, 47498, 474729, 4567]}]
    
    with donor_db._client as client:
        db = client[donor_db.database_name][donor_db.collection_name]
        db.insert_many(donor_data)
