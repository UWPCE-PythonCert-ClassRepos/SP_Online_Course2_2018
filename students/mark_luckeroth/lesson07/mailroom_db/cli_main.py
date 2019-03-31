#!/usr/bin/env python3

import os
from donor_models import Donor_obj
from mailroom_db_model_2 import *

MAIN_PROMPT = ("\nWould you like to:\n"
               "1 - Send a Thank You\n"
               "2 - Create a Report\n"
               "3 - Modify or Delete donor information\n"
               "4 - Modify or Delete a donation for a specific donor\n"
               "5 - Quit\n")


def list_donors():
    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = Donor.select(Donor.donor_name)
        donor_list = [donor.donor_name for donor in query]

    except Exception as e:
        pass

    finally:
        database.close()
    return donor_list


def add_donor(donor_name):
    """
    add person data to database
    """
    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_person = Donor.create(
                    donor_name = donor_name)
            new_person.save()

    except Exception as e:
        pass

    finally:
        database.close()


def add_donation(donation_amount, donor_name):
    """
    add donation data to database
    """
    database = SqliteDatabase('mailroom.db')
    if donor_name not in list_donors():
        add_donor(donor_name)

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_donation = Donation.create(
                amount = donation_amount,
                donor_name = donor_name)
            new_donation.save()

    except Exception as e:
        pass

    finally:
        database.close()


def select_donor():
    """
    delete a donation from database
    """
    while True:
        search_name = input('Please enter the name of a donor to modify: \n'
                            'for a list of donors, type "list": ')
        if search_name == 'list':
            print(list_donors())
            continue
        else:
            break

    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    query = Donor.select().where(Donor.donor_name.contains(search_name))
    print('The following entries matched your search: \n')
    print('{:<5s}|{:^20}|{:^12}'.format('#', 'Donor Name', 'Entry Date'))
    for i, donor in enumerate(query):
        print('{:<5}|{:^20}|{:^12}'.format(i, donor.donor_name,
                                            donor.initial_entry_date))
    print('\n')
    while True:
        index = int(input('choose the index number from the first column \n'
                      'above that matches the record you want to modify: '))
        if index not in list(range(len(query))):
            print('input must be one of the numbers in the first column above')
            continue
        else:
            break
    database.close()
    return str(query[index].donor_name)


def modify_donor():
    """
    delete a donation from database
    """

    donor_name = select_donor()

    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    while True:
        new_value = input('input the new name for the donor \n'
                          'OR enter "delete" to delete the donor record \n'
                          'CAUTION: DELETING THE DONOR WILL ALSO DELETE ALL DONATIONS FOR THIS DONOR:  ')
        if new_value.lower() == 'delete':
            mod_donor = Donor.get(Donor.donor_name == donor_name)
            mod_donor.delete_instance(recursive=True)
            break
        else:
            add_donor(new_value)
            query = (Donor
                     .select(Donor.donor_name, Donation.amount)
                     .join(Donation)
                     .where(Donor.donor_name == donor_name))
            for donor in query:
                add_donation(donor.donation.amount, new_value)
            mod_donor = Donor.get(Donor.donor_name == donor_name)
            mod_donor.delete_instance(recursive=True)
            break

    database.close()


def modify_donation():
    """
    delete a donation from database
    """
    selected_name = select_donor()

    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    query = (Donation
             .select()
             .where(Donation.donor_name == selected_name))
    print('Records on file for the selected donor: \n')
    print('Donor Name: {}'.format(selected_name))
    print('{:<5s}|{:<16s}|{:>12}'.format('#', 'Donation Amount', 'Date Donated'))
    for i, donation in enumerate(query):
        print('{:<5}|{:<16}|{:>12}'.format(i, donation.amount, donation.donation_date))
    while True:
        index = int(input('choose the index number from the first column \n'
                      'above that matches the record you want to modify: '))
        if index not in list(range(len(query))):
            print('input must be one of the numbers in the first column above')
            continue
        else:
            break

    while True:
        new_value = input('input the new value for the donation amount \n'
                          'OR enter "delete" to delete the donation record: ')
        if new_value.lower() == 'delete':
            query[index].delete_instance()
            break
        else:
            try:
                donation_amount = float(new_value)
            except ValueError:
                print('input must be a numerical value or "delete"')
            else:
                query[index].amount = donation_amount
                query[index].save()
                break

    database.close()


def thanks():
    while True:
        donor_name = input('Please enter the Full Name of the donor: ')
        if donor_name == 'list':
            print(list_donors())
            continue
        else:
            break
    while True:
        try:
            donation_amount = float(input('Please enter the amount of the donation: '))
        except ValueError:
            print('input for the amount must be a numerical value ')
        else:
            break
    add_donation(donation_amount, donor_name)
    print(f'Dear {donor_name}:')
    print(f'Thank you for your donation of ${donation_amount:.2f} to our charity.')
    print(f'Your contribution will do a great deal to help our worthy cause')


def create_donor_obj(donor_name):
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON')

    query = (Donor
             .select(Donor.donor_name, Donation.amount)
             .join(Donation)
             .where(Donor.donor_name == donor_name))
    donation_list = [float(str(donor.donation.amount)) for donor in query]
    database.close()
    return Donor_obj(donor_name, donation_list)


def create_report():
    title_str = '{:<20s}|{:^13}|{:^11}|{:>13}'
    bar_str = '-'*60
    entry_str = '{:<20s} ${:>10.2f} {:>11d} ${:>10.2f}'
    report = [title_str.format('Donor Name', 'Total Given',
                               'Num Gifts', 'Average Gift'), bar_str]
    for donor_name in list_donors():
        donor = create_donor_obj(donor_name)
        report.append(entry_str.format(*(donor.donor_name,
                                         donor.total,
                                         donor.count, donor.average)))
        del donor
    return report


def report():
    for row in create_report():
        print(row)


def letters():
    for donor_name in list_donors():
        donor = create_donor_obj(donor_name)
        with open(donor.donor_name+'.txt', 'w') as outfile:
            outfile.write("Dear {:}, \n".format(donor.donor_name))
            outfile.write(f"Thank you for your accumulative donation of ${donor.total:.2f}. \n")
            outfile.write('Your contribution will do a great deal to help our worthy cause')
        del donor


def quit():
    print("Quitting program")
    return "exit menu"


def menu_selection(prompt, dispatch_dict):
    while True:
        try:
            response = input(prompt)
            if dispatch_dict[response]() == "exit menu":
                break
        except KeyError:
            print('input must be one of the following: 1, 2, 3, or 4:')


MAIN_DISPATCH = {
    '1': thanks,
    '2': report,
    '3': modify_donor,
    '4': modify_donation,
    '5': quit
}

if __name__ == '__main__':
    menu_selection(MAIN_PROMPT, MAIN_DISPATCH)