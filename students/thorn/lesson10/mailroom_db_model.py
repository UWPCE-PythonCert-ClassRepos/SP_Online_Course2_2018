"""
Model for mailroom database structure.

Creates tables and fills in base data with sample data.
"""

import logging
import os
from peewee import *

logger = logging.getLogger(__name__)
FORMAT = "%(filename)s : %(levelname)s : %(lineno)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

database = SqliteDatabase('mailroom_database.db')

class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """ Information about indiviudal donors. """
    name = CharField(primary_key=True, max_length=20, null=False)  #primary key
    total_donation_amt = FloatField(null=True)
    avg_donation = FloatField(null=True)
    num_donations = FloatField(null=True)


class Donation(BaseModel):
    """ Information about donor donations. """
    donation_amt = FloatField(null=True)
    donor = ForeignKeyField(Donor, null=False, related_name="donors_info")


# Setup DB w/ sample data:
if __name__ == "__main__":
    # Delete old db
    if os.path.isfile('mailroom_database.db'):
        try:
            os.remove('mailroom_database.db')
        except PermissionError:
            logging.error("Database exists and is in use.  Close and retry.")

    # Create new db
    logging.info("Creating database.")
    donor_dict = {
    "Tom Horn": [599.23, 1000.00],
    "Theo Hartwell": [0.01, 0.01, 0.1],
    "Bailey Kimmitt": [8723.22, 27167.22, 91817.66],
    }

    try:
        database.connect()
        database.execute_sql("PRAGMA foreign_keys = ON;")

        # Create tables
        try:
            database.create_tables([Donor, Donation])
        except Exception as e:
            logger.error(f"Tables not created. {e}")
        finally:
            database.close()

        logger.info("Database created.  Populating fields from sample data.")
        for key, value in donor_dict.items():
            with database.transaction():
                # Populate Donor fields: name, average donation, total donation amount, number of donations
                donor = Donor.create(
                    name = key,
                    total_donation_amt = sum(value),
                    avg_donation = sum(value) / len(value),
                    num_donations = len(value)
                )
                donor.save()

                # Populate Donation fields: donation amount, donor
                for number in value:
                    donation = Donation.create(
                        donation_amt = number,
                        donor = key
                    )
                donation.save()

        for donor in Donor:
            logger.info(f"{donor.name} | {donor.total_donation_amt} | {donor.avg_donation} | {donor.num_donations}")
        # for donation in Donation:
            # logger.info(f"{donation.donor} | {donation.donation_amt}")

    except Exception as e:
        logger.error(f"Error creating database.  {e}")
    finally:
        database.close()

