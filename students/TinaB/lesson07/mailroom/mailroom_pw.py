import decimal
import logging
from datetime import datetime
import os
from donor_database_functions import *
from peewee import *
from mailroom_model import *
from pprint import pprint as pp
from donor_df import *


database = SqliteDatabase('donor_database.db')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Action
# donor_totals_list = get_all_donor_totals() #fullname, donation_total (sum donations), num_donations(count donations)
# donor_donations_list = get_list_of_donations() #donation_date, fullname, donationamount
# donor_names_list = get_list_of_donors() #firstname, lastname, fullname
# last_donation_list = get_max_donation_date_list() # fullname, last_donation_date, last_donation


def update_lists():
    """Refreshes the global list - to keep data fresh with additions and deletions from usage"""
    global donor_totals_list
    global donor_donations_list
    global donor_names_list
    global last_donation_list
    donor_totals_list = get_all_donor_totals()
    donor_donations_list = get_list_of_donations()
    donor_names_list = get_list_of_donors()
    last_donation_list = get_max_donation_date_list()


update_lists()

"""Print to screen/Report Functions"""
def print_donor_totals_report():
    """Print report to match example from assignment for donor list """
    # # Creating list to hold donors info for printing
    update_lists()
    try:
        print()
        title = ['Donor Name', '|  Total Given ', '|   Num Gifts',
                 '  | Average Gift']
        print('{:<20}{:>14}{:^14}{:>14}'.format(title[0], title[1],
                                                title[2], title[3]))
        print('-'*65)
        print()
        for donor in donor_totals_list:
            average_gift = float(donor.donation_total) / donor.num_donations
            print('{:<22}{}{:>12.2f}{:>10}{:>8}{:>12.2f}'.format(donor.fullname, '$', donor.donation_total,
                                                                 donor.num_donations, '$', average_gift))
        print()

    except Exception as e:
        logger.info(f'Error printing donor list at {donor.fullname}')
        logger.info(e)


def print_donors_names():
    """ prints list of donors names."""
    update_lists()
    print("\nDonors")
    print("-"*20)
    for donor in donor_names_list:
        print(donor.fullname)
    print()

def single_donor_print(donor_name):

    print()
    print(f'\nList of Donors and Donations for:{donor_name}')
    print("\nDonation Date - Donation Amount:")
    print("-"*40)
    for donation in donor_donations_list:
        if donation.fullname == donor_name:
            print('{} - ${:,.2f}'.format(donation.donation_date,
                                         donation.donation_amount))
    print()

def print_single_donor_donations():
    """ prints a list of a single donor and that donors donation history.
    Donor provided by user input.
    """
    update_lists()
    donor_name = get_name_input()
    single_donor_print(donor_name)
    return donor_name


def print_all_donor_donations():
    """ prints list of donors and thier donations to screen"""
    print("\nList of Donors and Donations")
    print("\nDonor Name - Donation Date - Donation Amount:")
    print("-"*40)
    for donation in donor_donations_list:
        print(f'{donation.fullname} - {donation.donation_date} - ${donation.donation_amount:,.2f}')
    print()


def print_report_df(input_list):
    print()
    title = ['Donor Name', '|  Total Given ', '|   Num Gifts',
             '  | Average Gift']
    print('{:<20}{:>14}{:^14}{:>14}'.format(title[0], title[1],
                                            title[2], title[3]))
    print('-'*65)
    print()
    # # Creating list to hold donors info for printing
    for donor in input_list:
        print('{:<22}{}{:>12.2f}{:>10}{:>8}{:>12.2f}'.format(donor.fullname, '$',
                                                             donor.donations_total_d(), donor.donation_count_d(),
                                                             '$', donor.average_donation_d()))
    print()


def send_letters_everyone():
    """Creates a letter for everyone in the database, and writes them to file."""
    update_lists()
    letters_count = 0
    date = datetime.now()
    new_folder = date.strftime("%Y-%m-%d_%H-%M")
    try:
        os.mkdir(new_folder)
    except OSError:
        print("\nError with directory creation.Something must have gone wrong!\n")
        return
    for donor in last_donation_list:
        # create file in date folder titled with donor name
        filename = "./{}/{}_{}.txt".format(new_folder,
                                           donor.fullname, donor.last_donation_date)
        with open(filename, 'w') as donor_thanks:
            letter_output = print_thank_you_total(donor)
            donor_thanks.write(letter_output)
        letters_count += 1
    print("Created {} Thank You letters in this folder: {}".format(
        letters_count, new_folder))


def print_letters_to_everyone():
    '''tests the print all function by printing letters to screen'''
    update_lists()
    print()
    for donor in last_donation_list:
        print(print_thank_you_total(donor))


def print_thank_you_total(donor):
    """ prints thank you message"""
    # donor comes in with last donation date , last_donation and fullname
    # pull donor total form global total list -
    for d in donor_totals_list:
        if d.fullname == donor.fullname:
            donation_total = d.donation_total

    thank_you = '''\n\nDear {}

    Thank you for your most recent generous donation of ${:,.2f}. You're support of ${:,.2f}
    over the years has helped us fund many great programs! We wanted to write you to thank you and that we 
    look forward to your continued support!

    Sincerely,

    The ChickTech Donations Department'''.format(donor.fullname, donor.last_donation, donation_total)
    return thank_you


def send_single_thank_you():
    """function for sending thank you message- gets/ adds single donation and prints thank you"""
    update_lists()
    donor_name = get_name_input()

    if donor_name == "quit":
        print("No donor name entered, exiting to menu")
    else:
        donor_amount = check_number_input()

        if donor_name not in donor_totals_list:
            firstname, lastname = donor_name.split(" ")
            add_donor(firstname, lastname, donor_name)
            add_donation(donor_name, donor_amount)
        else:
            for donor in donor_totals_list:
                if donor.fullname == donor_name:
                    add_donation(donor_name, donor_amount)
        print('\nDear {},'.format(donor_name))
        print('''\tThank you for your generous donation of ${:,.2f}\n
            Sincerely, \nThe ChickTech Donations Department\n'''.format(
            donor_amount))
    update_lists()


def get_name_input():
    ''' Function to select user input to return to print function
        USER INTERACTION'''
    name_input = input(
        "Please enter the name of the donor:  ")

    for donor in donor_names_list:
        if name_input.lower() in donor.fullname.lower():
            donor_check = input(
                "Is this the donor you are looking for: {}?\nPlease type yes or no >> ".format(
                    donor.fullname))
            if donor_check == 'yes':
                return donor.fullname

    print("{} is not in our records. Let's add {} to our list!".format(
        name_input, name_input))
    while True:
        new_donor_name = input(
            "Please enter the full name of the donor or type 'exit' to quit>> ")
        if new_donor_name == 'exit':
            return "quit"
        name_check = input(
            "Is this the donor name you would like to add: {} ?\nPlease type yes, no, or exit' to quit>> ".format(new_donor_name))
        if name_check == 'yes':
            print("Adding {} to donor list".format(new_donor_name))
            return new_donor_name
        elif name_check == 'exit':

            return "quit"
        else:  # anything other then yes
            print(
                "Let's try entering the donor name again. Or type 'exit' to quit to menu.")

def update_donation():
    """function to update a donation for a donor. 
    starts with printing that donor's donations
    """
    print()
    print('Welcome to the Update a Donor Donation Menu')
    print()
    donor_name = get_name_input()
    single_donor_print(donor_name)
    print('See the donation you want to change in the report? Follow the prompts to enter donation to change')
    old_donation_amount = check_number_input()
    print('Please follow the prompts to enter the amount you would like to update the donation to')
    new_donation_amount = check_number_input()
    print()
    #Call db function with donor_name, donation to change, input to update
    change_donation(donor_name,old_donation_amount,new_donation_amount)
    print('Donation has been updated. See report below for verification')
    single_donor_print(donor_name)

def delete_donation():
    """function to delete a donation for a donor. 
    starts with printing that donor's donations
    """
    print()
    print('Welcome to the Delete a a Donor Donation Menu')
    print()
    donor_name = get_name_input()
    single_donor_print(donor_name)
    print('See the donation you want to delete in the report? Follow the prompts to enter donation to delete')
    donation_delete = check_number_input()
    print()
    delete_donation_from_db(donor_name,donation_delete)
    print('Donation has been deleted. See report below for verification')
    single_donor_print(donor_name)

def add_a_donor():
    """Adds a Donor to the list - but not a donation"""
    print()
    print('Welcome to the Add a Donor Menu')
    print()
    donor_name = get_name_input()
    firstname, lastname = donor_name.split(' ')
    add_donor(firstname, lastname, donor_name)
    print('Added Donor to our database. See below for updated database list')
    print_donors_names()


def check_number_input():
    '''Error Handling: Checks if number was entered by converting the number to a float'''
    while True:
        try:
            number = float(input('Please enter a donation amount : '))
        except ValueError:
            print("Please enter a number for donation amount!")
        else:
            if number > 0.0:
                return number
            else:
                print('Please enter a donation amount above 0.')


""" Get/Collect Data Functions"""


def create_donors_list():
    donor_class_list = []
    for donor in donor_names_list:
        donor_donations = []
        for donation in donor_donations_list:
            if donation.fullname == donor.fullname:
                donor_donations.append(float(donation.donation_amount))
        if donor_donations:
            donor_class_list.append(
                Donor(donor.firstname, donor.lastname, donor.fullname, donor_donations))
    return donor_class_list


""" Menu Options and Set Up Section"""


def menu_selection(menu_input, user_entry):
    """menu function"""
    try:
        menu_input[user_entry]['menu_dispatch']()
    except KeyError:
        print("{} is not a valid choice. ".format(user_entry))
        return False
    else:
        return True


def main_menu():
    '''Create Main Menu'''
    main_menu_title = "\nWelcome to the Mailroom App\nWhat would you like to do?\n"
    print_menu_options(MAIN_MENU, main_menu_title)


def print_menu_options(menu_input, menu_title):
    ''' Prints  Menu'''
    while True:
        print(menu_title)
        for key, value in menu_input.items():
            # prints each option and then prompts for user input
            print(key, value['menu_prompt'])
        response = input("\nEnter a number or q to exit menu>>>  ")
        menu_selection(menu_input, response)
        if response == 'q':
            return


def thank_you_menu():
    '''Create Send a Thank you sub Menu'''
    single_print_menu_title = "\nWelcome to Donor Interaction Menu:\nWhat would you like to do: \n"
    print_menu_options(SEND_A_THANK_YOU_SUB_MENU, single_print_menu_title)


def single_print_menu():
    '''Create single print sub Menu'''
    single_print_menu_title = "\nWelcome to the Single Print Menu:\nWhat would you like to do: \n"
    print_menu_options(SINGLE_PRINT_SUB_MENU, single_print_menu_title)


def quit_menu():
    '''Quit menu function and method'''
    print("Quitting this menu now")
    return "exit menu"


"""
Challenge and Projection Code
"""
def challenge():
    """
    #####Called from Menu
    Gets user input for donations muliplier challenge.
    Prints the list to screen for added fun!
    """
    challenge_list = create_donors_list()
    logger.info(f'printing created list')
    print_report_df(challenge_list)
    print()
    print('''Welcome to the Challenge Option. Here you can multiply all donations by any number,
        or you can multiply donations within an optional min and max donation amount.
        ''')
    try:
        minimum_input = float(
            input('Enter a minimum donation amount (0 if none):  '))
        maximum_input = float(
            input('Enter a maximum donation amount (0 if none):  '))
        factor = float(
            input('Please enter the factor you wish to multiply these donations by >>  '))
    except ValueError:
        print('Please follow instructions and enter a number only')

    new_donor_list = challenge_functions(
        challenge_list, factor, minimum_input, maximum_input)
    # Printing list for fun
    logger.info(f'printing challenge list')
    print_report_df(new_donor_list)
    return new_donor_list


def challenge_functions(input_list, factor, min_don=None, max_don=None):
    """Returns a new db of donors multiplied by the factor provided. 
        Creates new db calling the filter_factor_map"""

    new_challenge_list = []
    for donor in input_list:
        # print(donor.donations)
        donation = filter_factor_map(factor, donor.donations, min_don, max_don)
        if donation:
            new_challenge_list.append(
                Donor(donor.firstname, donor.lastname, donor.fullname, donation))
    return new_challenge_list


def filter_factor_map(factor, donations, min_donation=None, max_donation=None):
    """Uses filter, map and the factor to provide the new list of filtered donations"""
    if min_donation and max_donation:
        if min_donation > max_donation:
            raise ValueError(
                'Minimum Donation listed is larger than Maximum Donation. Try Again!')
        else:
            return list(map(lambda x: x * factor,
                            filter(lambda y: min_donation <= y <= max_donation, donations)))
    elif min_donation:
        return list(map(lambda x: x * factor,
                        filter(lambda y: y >= min_donation, donations)))
    elif max_donation:
        return list(map(lambda x: x * factor,
                        filter(lambda y: y <= max_donation, donations)))
    else:
        return list(map(lambda x: x * factor, donations))


def projection(input_list, factor, min_donation=None, max_donation=None):
    """Return projection value for donations. a feature that could show them, 
    based on past contributions, what their total contribution would become under different scenarios
    """
    projected_contribution = 0
    for donor in input_list:
        projected_contribution += sum(filter_factor_map(factor,
                                                        donor.donations,
                                                        min_donation,
                                                        max_donation))
    # returns the projection
    return projected_contribution


def projected():
    """Gets user input for projection muliplier functionality. Takes min and max and prints contribution."""
    # pull updated list of donors(class)
    projected_list = create_donors_list()
    print('''Welcome to the Projection Option. Here you can run projections for contributions. 
        Help Companies structure their matching donations based on past contribution amounts.
        Simply enter the minumum and maximum donation range that will be matched and see the total contribution:''')
    try:
        minimum_input = float(
            input('Enter a minimum donation amount (0 if none):  '))
        maximum_input = float(
            input('Enter a maximum donation amount (0 if none):  '))
        factor = float(
            input('Please enter the factor you wish to multiply these donations by >>  '))
    except ValueError:
        print('Please follow instructions and enter a number only')

    projections = projection(projected_list, factor,
                             minimum_input, maximum_input)
    print('\nProjected contribution value: ${:,.2f}'.format(projections))



#------Menu Dictionaries of Dictionaries .Needs to be after the functions or code won't work. ------
MAIN_MENU = {
    "1": {'menu_prompt': 'Donor Functions Menu - Add, Update, Thank or Delete', 'menu_dispatch': thank_you_menu},
    "2": {'menu_prompt': 'Quick Report of our Donors', 'menu_dispatch': print_donor_totals_report},
    "3": {'menu_prompt': 'Report Menu', 'menu_dispatch': single_print_menu},
    "4": {'menu_prompt': 'Send Letters to Everyone', 'menu_dispatch': send_letters_everyone},
    #"5": {'menu_prompt': 'Test Print All', 'menu_dispatch': print_letters_to_everyone},
    "6": {'menu_prompt': 'Donation Challenge', 'menu_dispatch': challenge},
    "7": {'menu_prompt': 'Create Projection for Donations', 'menu_dispatch': projected},
    "q": {'menu_prompt': 'Quit Program', 'menu_dispatch': quit_menu}
}

SEND_A_THANK_YOU_SUB_MENU = {
    "1": {'menu_prompt': 'Lookup Donor By Name to send a Thank You', 'menu_dispatch': send_single_thank_you},
    "2": {'menu_prompt': 'Print List of Donors', 'menu_dispatch': print_donors_names},
    "3": {'menu_prompt': 'Update/Edit a donation', 'menu_dispatch': update_donation},
    "4": {'menu_prompt': 'Delete a donation', 'menu_dispatch': delete_donation},
    "5": {'menu_prompt': 'Add a Donor', 'menu_dispatch': add_a_donor},
    #"6": {'menu_prompt': 'Delete a donation', 'menu_dispatch': delete_donor},
    "q": {'menu_prompt': 'Quit to Main Menu', 'menu_dispatch': quit_menu}}

SINGLE_PRINT_SUB_MENU = {
    "1": {'menu_prompt': 'Print List of Donors', 'menu_dispatch': print_donors_names},
    "2": {'menu_prompt': 'Print Donors and All Donations', 'menu_dispatch': print_all_donor_donations},
    "3": {'menu_prompt': 'Print A Donors Donation History', 'menu_dispatch': print_single_donor_donations},
    "q": {'menu_prompt': 'Quit to Main Menu', 'menu_dispatch': quit_menu}}


if __name__ == '__main__':
    main_menu()
