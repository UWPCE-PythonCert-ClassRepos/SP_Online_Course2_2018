#!/usr/bin/env python3
import sys
from collections import defaultdict
import donor_model as dm
import logging

"""class Donor:

    def __init__(self, name, donations=None):

        self.name = name
        if donations is None:
            self.donations = []
        else:
            self.donations = donations


    def add_donation(self, amount):
        try:
            self.donations.append(int(amount))
        except ValueError:
            print("Please enter a number!")


    def number_donations(self):
        return len(self.donations)


    def total_donation(self):
        try:
            return sum(self.donations)
        except TypeError:
            return self.donations

    def avg_donation(self):
        try:
            return self.total_donation()/ self.number_donations()
        except TypeError:
            return self.donations"""

'''class Roster:

    def __init__(self, donors=None):
        self.donor_list = donors'''

def create_donor_list():
    database = dm.SqliteDatabase('donors.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        return [donor.donor_name for donor in dm.Donor.select()]
        # data = (dm.Donor.select(dm.Donor, dm.Donation).join(dm.Donation, dm.JOIN.INNER))

    except Exception as e:
        logger.info(e)
    finally:
        database.close()


def create_donor_tables():
    database = dm.SqliteDatabase('donors.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (dm.Donor
                 .select(dm.Donor, dm.Donation)
                 .join(dm.Donation, dm.JOIN.INNER)
                 )

        donor_names = []
        d_report = []

        for donor in dm.Donor.select():
            donor_names.append(donor.donor_name)

        for name in donor_names:
            donation_amounts = []
            for data in query:
                if data.donor_name == name:
                    donation_amounts.append(data.donation.donation_amount)

            d_report.append([name, int(sum(donation_amounts)), len(donation_amounts)])


        return d_report

    except Exception as e:
        logger.info(e)
    finally:
        database.close()


def thank_you():
    '''Accepts user input, and then adds donors / donations to the donor dictionary.
    It also prints a thank you message for the latest donation'''
    print('Please enter the donor name\n (Type "list" for a list of current donor names)\n '
        'Press "q" to return to console')

    donor_list = list(create_donor_list())
    new_donor = input(':')

    if new_donor.lower() == 'list':
       # donor_names = []
       # for donor in donor_list:
       #     donor_names.append(donor.name)
        print("\n".join(sorted(create_donor_list())))

    elif new_donor.lower() == 'q':
        return

    else:
        if new_donor in donor_list:
            try:
                amount = float(input('Please enter the donation amount:'))
                # donor_list[new_donor].add_donation(amount)
                add_donor(new_donor, amount)
                print('Thank you {} for your generous donation of ${:.2f}'.format(new_donor, amount))
            except ValueError:
                print("Please enter a round number!")
        else:
            amount = float(input('Please enter the donation amount for the new donor:'))
            # new_donor_object = Donor(new_donor, [amount])
            add_donor(new_donor, amount)
            print('Thank you {} for your generous donation of ${:.2f}'.format(new_donor, amount))

def donor_report():
    '''Outputs a string that is a table of the donors and contributions'''
    print('Here is a list of donors and contributions')
    report = create_donor_tables()
    print("\nDonor Name           |  Total Donated | Number Donations | Average Gift")
    print("--------------------------------------------------------------------------\n")

    for donor_report in report:
        print("{:22}{:15.2f}{:15}   {:13.2f}".format(donor_report[0], donor_report[1],donor_report[2],donor_report[1] / donor_report[2]))
    print("\n")

    #report.append('|{:<20}|{:<20}|{:<20}|{:<20}|'.format('Name', 'Total', 'Donations', 'Average'))
    #for donor_name in report:
    #    report.append('|{:<20}|{:>20}|{:>20}|{:>20}|'.format(donor_name[0], donor_name[1], donor_name[1], donor_name[1]/donor_name[2]))
    #return '\n'.join(report)

def print_donors():
    print(donor_report())
    #print(create_donor_tables())

def add_donor(name, amount):
    database = dm.SqliteDatabase('donors.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        if name not in create_donor_list():
            with database.transaction():
                new_donor = dm.Donor.create(
                    donor_name = name,
                    donor_num = int(len(list(create_donor_list())))+1
                    )
                print("{} is a new donor. Yay!".format(name))
        with database.transaction():
            new_gift = dm.Donation.create(
                donation_amount = amount,
                donor_name_two = name
                )
            new_gift.save()
            print('Donation ${} added for {}'.format(amount, name))

    except Exception as e:
        logger.info(e)
    finally:
        database.close()

def delete_donor():
    delete_name = input("Who do you want to delete? \n")

    database = dm.SqliteDatabase('donors.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donor_name_list = [donor.donor_name for donor in dm.Donor.select()]

        if delete_name in donor_name_list:
            donor_delete = dm.Donor.get(dm.Donor.donor_name == delete_name)
            donor_delete.delete_instance()
            donor_delete = dm.Donation.get(dm.Donation.donor_name_two == delete_name)
            donor_delete.delete_instance()
            print("{} has been deleted.".format(delete_name))

        else:
            print("Who?")

    except Exception as e:
        logger.info(e)
    finally:
        database.close()



#def batch_file():
    #'''Creates a text file with a thank you message for each of the donors in the dictionary'''
    #for donor_data in self.donor_list:
    #    filename = donor_data.name.replace(" ", "_") + ".txt"
    #    total_donation = donor_data.total_donation()
    #    letter = ('Thank you {} for you generous contributions totalling {:.2f}!'.format(donor_data.name, total_donation))
    #    with open(filename, 'w') as letter_file:
    #        letter_file.write(letter)
    #    print(f"{donor_data.name}'s letter has been saved to " + filename)


def menu_selection(prompt, dispatch_dict):
    '''Creates a menu that accepts user input and then selects a function based on that input'''
    while True:
        try:
            response = input(prompt)
            dispatch_dict[response]()
        except KeyError:
            print('Please enter a valid selection from the menu')

def quit_console():
    sys.exit("Exiting the program")

if __name__ == '__main__':

    '''Andy = Donor('Andy', [10.00])
    Bill = Donor('Bill', [15.00, 25.00])
    Chuck = Donor('Chuck', [20.00, 30.00, 40.00])
    mailroom = Roster([Andy, Bill, Chuck])'''


    console_prompt = ("\nWelcome to the Donor Tracking System\n"
                      "Please press a number to make a selection\n"
                      "1.) Send a thank you note\n"
                      "2.) Create a Report\n"
                      "3.) Delete a Donation\n"
                      "4.) Quit(press 'q')\n")

    console_dict = {'1': thank_you,
                    '2': donor_report,
                    '3': delete_donor,
                    '4': quit_console,
                    'q': quit_console,
                    'Q': quit_console}


    menu_selection(console_prompt, console_dict)