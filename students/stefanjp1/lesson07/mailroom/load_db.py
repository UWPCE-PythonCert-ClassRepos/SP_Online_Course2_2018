from db_model import *


def populate_db():
    """
    add donor and donation data to database
    """

    database = SqliteDatabase('mailroom.db')

    DONOR_NAME = 0

    people = [
        'Andrew',
        'Peter',
        'Susan',
        'Pam',
        'Steven',
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in people:
            with database.transaction():
                new_donor = Donor_Records.create(donor_name=donor)

        for saved_person in Donor_Records:
            print(f'New Donor: {saved_person.donor_name}')

    except Exception as e:
        print(f'Error creating = {person}')
        print(e)

    finally:
        database.close()


    #Work with the Donation class
    database = SqliteDatabase('mailroom.db')

    DONOR = 0
    DONATION_AMT = 1

    donations = [
        ('Andrew', 20),
        ('Peter', 100),
        ('Susan', 30),
        ('Pam', 10),
        ('Pam', 25)
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_donation=Donation_Records.create(
                    donor=donation[DONOR],
                    donation_amt=donation[DONATION_AMT])
                new_donation.save()
            print('Donor {} donated ${}'.format(donation[DONOR],
                                                      donation[DONATION_AMT]))

        for saved_person in Donation_Records:
            print(f'New Donation: {saved_person.donor}, ${saved_person.donation_amt}')

    except Exception as e:
        print(e)

    finally:
        database.close()


if __name__ == '__main__':
    populate_db()
