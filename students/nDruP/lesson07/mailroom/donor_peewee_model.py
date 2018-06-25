from peewee import *
from functools import partial


donor_db = SqliteDatabase('donor.db')
MoneyField = partial(DecimalField, decimal_places=2)


class BaseModel(Model):
    class Meta:
        database = donor_db


class Donation(BaseModel):
    donor = CharField(max_length=30, unique=False)
    gift = MoneyField()


if __name__ == '__main__':
    donor_db.connect()
    donor_db.execute_sql('PRAGMA foreign_keys=ON;')
    with donor_db as db:
        db.create_tables([Donation])
    
    donor_history = [('Sleve McDichael',[86457.89,2346.43,9099.09]),
                     ('Willie Dustice', [505.05,43.21]),
                     ('Rey McScriff', [666.0]),
                     ('Mike Truk', [70935.3,12546.7,312.0]),
                     ('Bobson Dugnutt', [1234.56,789.0]),
                     ('Todd Bonzalez',[10352.07,2394.32]),
                     ('andrew', [9473.65])]
    try:
        donor_db.connect()
        donor_db.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, history in donor_history:
            for gift in history:
                with donor_db.transaction():
                    new_donation = Donation.create(donor = donor, gift = gift)
                    new_donation.save()
    except Exception as e:
        print(e)
    finally:
        donor_db.close()
