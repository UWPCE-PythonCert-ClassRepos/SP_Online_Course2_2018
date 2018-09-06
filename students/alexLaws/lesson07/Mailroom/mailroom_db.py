from peewee import *

database = SqliteDatabase('donation_records.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Donor_Records(BaseModel):
    full_name = CharField(max_length=60)

class Donation_Records(BaseModel):
    donor = ForeignKeyField(Donor_Records, related_name='donated', null=False)
    donation_amt = IntegerField()


database.create_tables([Donor_Records, Donation_Records])
database.close()
