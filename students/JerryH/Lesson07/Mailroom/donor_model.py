"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from functools import partial
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('donors.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')


MoneyField = partial(DecimalField, decimal_places=2)

class Donor(BaseModel):
    """
        This class defines Donor.
    """
    # donor_id = IntegerField(primary_key = True)
    # first_name = ChrFaield(max_length = 15)
    # last_name = CharField(max_length = 15)
    donor_name = CharField(primary_key = True, max_length = 50)
    donor_id = IntegerField()


class Donation(BaseModel):
	"""
		This class defines Donations.
	"""
	gift_value = MoneyField()
	gift_donor = ForeignKeyField(Donor, column_name = 'donor_name', null = False)



database.create_tables([
        Donor,
        Donation
    ])

database.close()



def populate_donors():
	"""
		Add donor to database
	"""

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	database = SqliteDatabase('donors.db')

	logger.info('Working with Donor class')

	DONOR_NAME = 0
	DONOR_ID = 1

	donors = [
		('Bill Gates', 1),
		('Jeff Bezo', 2),
		('Mike Dell', 3),
		('Harry Potter', 4),
		('Ben Williams', 5)
	]

	try:
		database.connect()
		database.execute_sql('PRAGMA foreign_keys = ON;')
		for donor in donors:
			with database.transaction():
				new_donor = Donor.create(
					donor_name = donor[DONOR_NAME],
					donor_id = donor[DONOR_ID]
					)
			new_donor.save()
			logger.info('Database add successful')

		logger.info('Print the Donor records we saved...')

		for saved_donor in Donor:
			logger.info(f'{saved_donor.donor_name} added to database.')

	except Exception as e:
		logger.info(f'Error creating = {donor[DONOR_NAME]}')
		logger.info(e)
		logger.info('See how the database protects our data')

	finally:
		logger.info('database closes')
		database.close()



def populate_donations():
	"""
		Add donations to database
	"""

	database = SqliteDatabase('donors.db')

	GIFT_VALUE = 0
	GIFT_NAME = 1

	donations = [
		(234.22, 'Bill Gates'),
		(400.32, 'Bill Gates'),
		(2345.23, 'Jeff Bezo'),
		(82934.25, 'Jeff Bezo'),
		(9883.23, 'Jeff Bezo'),
		(245.99, 'Mike Dell'),
		(9345.23, 'Harry Potter'),
		(235.13, 'Ben Williams'),
		(2459.44, 'Harry Potter'),
		(1345.20, 'Ben Williams'),
	]

	try:
		database.connect()
		database.execute_sql('PRAGMA foreign_keys = ON;')
		for donation in donations:
			with database.transaction():
				new_gift = Donation.create(
					gift_value = donation[GIFT_VALUE],
					gift_donor = donation[GIFT_NAME])
				new_gift.save()
				logger.info('Database add successful')

			logger.info('Print the Person records we saved...')
		for saved_donation in Donation:
			logger.info(f'{saved_donation.gift_value} from {saved_donation.gift_donor}')

	except Exception as e:
		logger.info(f'Error creating = {donation[GIFT_VALUE]}')
		logger.info(e)
		logger.info('See how the database protects our data')

	finally:
		logger.info('database closes')
		database.close()

if __name__ == '__main__':
    populate_donors()
    populate_donations()




