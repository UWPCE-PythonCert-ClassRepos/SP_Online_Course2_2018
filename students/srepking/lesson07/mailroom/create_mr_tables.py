import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase(None)
#database = SqliteDatabase('mailroom.db')
#database.connect()
#database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database



class Donor(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    donor_name = CharField(primary_key=True, max_length=30)

class Donations(BaseModel):
    """
        This class hold donations.
    """

    donor_name = ForeignKeyField(Donor)
    donation = DecimalField(max_digits=100, decimal_places=2)



#logger.info('Creating mailroom.db database.')
#database.create_tables([Donor, Donations])
#database.close()
