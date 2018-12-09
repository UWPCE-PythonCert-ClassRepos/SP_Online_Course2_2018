from peewee import *
database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

# this fails
class Donor(BaseModel):
    donor_name = CharField(primary_key = True, max_length = 30)

# this works
# class Donor(BaseModel):
#     donor_name = CharField(max_length = 30)

database.create_tables([Donor])

new_donor = Donor.create(donor_name = "John Novak")

new_donor.save()

database.close()