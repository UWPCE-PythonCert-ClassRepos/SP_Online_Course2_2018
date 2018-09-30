"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema

"""

from peewee import *
import builtins

db_name = 'donors.db'
if hasattr(builtins, 'model_py_database_name_for_mailroom5_donors'):
    db_name = builtins.model_py_database_name_for_mailroom5_donors
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta(object):
        database = database


class DonorInfo(BaseModel):
    """Schema for a row encoding a donor."""
    name = CharField(primary_key = True, max_length = 60)
    last_name = CharField(max_length = 30)
    first_name = CharField(max_length = 30)


class Donation(BaseModel):
    """Schema for a donation.
    
    Does not use a primary key because this item is distinuished through its
    backpointer its DonorInfo entry.
    """
    donation = DoubleField()
    donor = ForeignKeyField(DonorInfo, related_name='was_filled_by', null = False)


def CreateTables():
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.create_tables([
            DonorInfo,
            Donation
        ])
    database.close()


def SaveDonorInfo(first_name, last_name):
    name = last_name + ',' + first_name
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            row = DonorInfo.create(
                name = name,
                last_name = last_name,
                first_name = first_name)
            row.save()
    except Exception as e:
        # Writing DonorInfo is expected to fail when it's previously been
        # written
        pass
    finally:
        database.close()


def SaveDonation(name, donation):
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            row = Donation.create(donation = donation, donor = name)
            row.save()
    except Exception as e:
        print(f'failed to write "{name}" to {db_name}')
        print(e)
    finally:
        database.close()

def UpdateDonation(name, old_donation, new_donation):
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            query = (Donation
                     .select()
                     .join(DonorInfo)
                     .where(Donation.donor == name)
                     .where(Donation.donation == old_donation))

            if len(query) == 0:
                print(f'WARN: UpdateDonation failed to find record for'
                      ' name={name} donation={old_donation}')
            else:
                row = query[0]
                if new_donation:
                    row.donation = new_donation
                    row.save()
                else:
                    row.delete_instance()
    except Exception as e:
        print(f'failed to update "{name}" from {old_donation}'
              f' to {new_donation}')
        print(e)
    finally:
        database.close()
