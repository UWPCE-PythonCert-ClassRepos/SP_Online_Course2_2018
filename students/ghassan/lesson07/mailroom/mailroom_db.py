import logging
from peewee import Model, CharField, ForeignKeyField, FloatField, IntegerField, SqliteDatabase


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Setting up the database')

database = SqliteDatabase('mailroom.db')

logging.info('Database {} is created'.format(database))


class BaseModel(Model):
    """
    BaseModel class for the db classes to inherit from
    """
    class Meta:
        database = database


class Donor(BaseModel):
    """
    Donor class
    """
    logger.info('Creating the Donor class')
    donor_name = CharField(primary_key=True)
    number_of_donations = IntegerField(null=True)
    total_donations = FloatField(null=True)


class Donations(BaseModel):
    """
    a class to map a donor with a donation
    """
    logger.info('Creating Donations class')
    d_name = ForeignKeyField(Donor, related_name='is_donated_by')
    donation_amount = FloatField()


database.create_tables([
        Donor,
        Donations
    ])

logger.info('Tables were created')

database.close()

logger.info('Database is closed')


# class Mailroom:
#
#     def __init__(self, donors):
#         self.donors = donors
#
#     def save_donors(self):
#         for donor in self.donors:
#             donor.save_data()
#
#     def load_donors(self):
#         _donors = []
#         donors_files = os.listdir('.')
#         donors_names = [z for z in donors_files if z.split('.')[-1] == 'json']
#         for donor in donors_names:
#             _donors.append(Donor.load_data(donor))
#         self.donors = _donors
#
#     def add_donor(self, donor):
#         self.donors.append(donor)
#
#     def get_donor(self, given_donor):
#         for donor in self.donors:
#             if donor.name == given_donor:
#                 return donor
#
#     def send_thankyou(self, donor_name):
#         donor = self.get_donor(donor_name)
#         return 'Thank you {} for your generous donation of {}'.format(
#             donor.name, donor.total_donations
#         )
#
#     def all_donors(self):
#         return [x.name for x in self.donors]
#
#     def list_donors(self):
#         return "\n".join(self.all_donors())
#
#     def create_report(self):
#         print('{:20} | {:15} | {:10} | {:15}'.format(
#             'Donor Name', 'Total Given', 'Num Gifts', 'Average Gift'))
#         print('-'*70)
#         for donor in self.donors:
#             print('{:20} | {:15} | {:10} | {:15}'.format(
#                 donor.name, donor.total_donations,
#                 donor.num_of_gifts,
#                 donor.total_donations / donor.num_of_gifts))
#
#     def save_report(self):
#         for donor in self.donors:
#             with open(donor.name+'.txt', 'w') as donorfh:
#                 donorfh.write(self.send_thankyou(donor.name))
