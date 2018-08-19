"""Script to set up sqlite database for mailroom. I decided to use
just one table to store all of the data. If I were storing more information
about the donors (age, address, email, etc) it would make sense to have
one table for donors and one for transactions, but I'm not. So creating 
multiple tables would have been redundant. Since neither donor nor 
donation amount is necessarily unique, I used a generated primary key"""

from peewee import *

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Transaction(BaseModel):
    """Stores donor name and transaction amount for each donation"""

    donor_name = CharField(max_length = 30)
    donation_amount = DecimalField(max_digits = 7, decimal_places = 1)

if __name__ == '__main__':
    database.create_tables([Transaction])