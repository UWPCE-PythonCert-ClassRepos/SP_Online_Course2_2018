from mailroom_model import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donors.db')
logger.info('Creating database.')

donor_list = {
        'John Smith': [18774.48, 8264.47, 7558.71],
        'Jane Doe': [281918.99, 8242.13],
        'Alan Smithee': [181.97, 955.16],
        'Tom D.A. Harry': [67.10, 500.98],
        'Joe Shmoe': [200.01]
        }


def populate_donors():
    """
    Populates donors in database using Donor class from mailroom_model.
    """

    logger.info('Adding donors to database...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, donations in donor_list.items():
            with database.transaction():
                new_donor = Donor.create(
                    donor_name=donor,
                    sum_donations=sum(donations),
                    number_donations=len(donations),
                    avg_donations=sum(donations)/len(donations)
                    )
                new_donor.save()
                logger.info('Database add successful.')
        logger.info('Printing records just added...')
        for saved_donor in Donor:
            logger.info(f'{saved_donor.donor_name} has donated {saved_donor.number_donations} times, for a total '
                        f'amount of ${saved_donor.sum_donations} and an average of ${saved_donor.avg_donations}.')

    except Exception as e:
        logger.info(f'Unable to add donor to database.')
        logger.info(e)

    finally:
        logger.info('Closing database.')
        database.close()


def population_donations():
    """
    Populates donations in database using Donation class from mailroom_model.
    """


# donor1 = Donor("John Smith", [18774.48, 8264.47, 7558.71])
# donor2 = Donor("Jane Doe", [281918.99, 8242.13])
# donor3 = Donor("Alan Smithee", [181.97, 955.16])
# donor4 = Donor("Tom D.A. Harry", [67.10, 500.98])
# donor5 = Donor("Joe Shmoe", [200.01])
#
# donor_db = DonorDatabase([donor1, donor2, donor3, donor4, donor5])

if __name__ == "__main__":
    populate_donors()
