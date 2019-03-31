"""
test code for donor_models.py

"""

from donor_db_model import *



def populate_donordata():
    """
    add donor data to database
    """

    database = SqliteDatabase('mailroom.db')

    people = [
        'Peter Pan',
        'Paul Hollywood',
        'Mary Berry',
        'Jake Turtle',
        'Raja Koduri'
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for name in people:
            with database.transaction():
                new_person = Donor.create(
                        donor_name = name)
                new_person.save()

        for saved_person in Donor:
            print(f'{saved_person.donor_name} has been saved')

    except Exception as e:
        print(f'Error creating = {name}')

    finally:
        print('database closes')
        database.close()


def populate_donationdata():
    """
    add donation data to database
    """

    database = SqliteDatabase('mailroom.db')

    donations = {
        'Peter Pan': [10., 10., 10., 10.],
        'Paul Hollywood': [5., 5000., 5., 5.],
        'Mary Berry': [100.],
        'Jake Turtle': [123., 456., 789.],
        'Raja Koduri': [60., 60000.]
        }

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor_name, donation_list in zip(donations.keys(), donations.values()):
            for donation in donation_list:
                with database.transaction():
                    new_donation = Donation.create(
                        amount = donation,
                        donor_name = donor_name)
                    new_donation.save()

        for saved_donation in Donation:
            print(f'{saved_donation.amount} has been donated by {saved_donation.donor_name}')

    except Exception as e:
        print(f'Error creating = {donation} donated by {donor_name}')

    finally:
        print('database closes')
        database.close()


def pprint_db():
    """
    Print summary of database to CLI
    """

    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Donor
                     .select(Donor, Donation)
                     .join(Donation, JOIN.LEFT_OUTER)
                    )

        print('**********************DATA SUMMARY*************************')
        print('\n')

        for donor in query:
            try:
                print(f'Person {donor.donor_name} made a donation of {donor.donation.amount}')

            except Exception as e:
                print(f'Person {donor.donor_name} made no donations')
        print('\n')
        print('********************END DATA SUMMARY***********************')

    except Exception as e:
        print(e)

    finally:
        database.close()


if __name__ == '__main__':
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
    database.create_tables([
        Donor,
        Donation
    ])
    database.close()

    populate_donordata()
    populate_donationdata()
    pprint_db()
