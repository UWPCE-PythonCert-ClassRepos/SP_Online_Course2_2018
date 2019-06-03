#-------------------------------------------------#
# Title: Database MailRoom
# Dev:   LDenney
# Date:  January 1, 2018
# ChangeLog: (Who, When, What)
#   Laura Denney, 10/11/18, Created MailRoom Part 1 File
#   Laura Denney, 10/12/18, Modified MailRoom Part 1 File
#   Laura Denney, 10/12/18, Started Part 2
#   Laura Denney, 10/12/18, Finished Part 2
#   Laura Denney, 10/31/18, Started MailRoom Part 3
#   Laura Denney, 11/7/18, Started MailRoom Part 4
#   Laura Denney, 12/7/18, Started Object Oriented Mail Room
#   Laura Denney, 12/17/18, Added Saving / Loading Functionality
#   Laura Denney, 1/1/19, Started Functional Programming MailRoom
#   Laura Denney, 5/10/19, Started Database MailRoom
#   Laura Denney, 5/10/19, Finished Database MailRoom
#-------------------------------------------------#

#importing models, logging, datetime, peewee
from mailroom_populate import *

#file handling help
import os

####################################################
####################################################

#Non-class variables and functions

dh = Database_Handler()

main_prompt = '''
What would you like to do today?
1) Send a Thank You
2) Create a Report
3) Send letters to everyone
4) See projections for matching contributions
5) Update Donation or Remove a Donor in the system
6) Quit
Please choose the number of your choice >> '''

thank_you_prompt = '''
You have chosen to Send a Thank You.
1) See List of Current Donors
2) I'm Ready to Thank a Donor
3) Quit this submenu
Please choose the number of your choice >> '''

update_prompt = '''
You have chosen to Update a Donation or Remove a Donor.
1) Update A Current Donor's Donation amounts
2) Remove a Donor and all their Donations
3) Quit this submenu
Please choose the number of your choice >>'''

yes_no_prompt = '''
1) Yes
2) No
Please choose the number of your choice >>'''

#************Map function
def map_projection(multiplier=0, min_donation=0, max_donation=0, projection_list=None):
    if min_donation and max_donation:
        filtered_list = list(filter(lambda x: x >= min_donation and x <= max_donation, projection_list))
    elif min_donation:
        filtered_list = list(filter(lambda x: x > min_donation, projection_list))
    elif max_donation:
        filtered_list = list(filter(lambda x: x < max_donation, projection_list))
    new_donations = list(map(lambda x: x * multiplier, filtered_list))
    return new_donations

def projections():
    projection_list = dh.projection_query()
    str_projections = '''
Current total donations to our cause: ${:.2f}
Your contribution if doubling contributions under $100: ${:.2f}
Your contribution if tripling contributions over $50: ${:.2f}
Your contribution if quadrupling contributions between $50 and $100: ${:.2f}
'''
    print(str_projections.
          format(
            sum(projection_list),
            sum(map_projection(2,max_donation = 100, projection_list = projection_list)),
            sum(map_projection(3,min_donation = 50, projection_list = projection_list)),
            sum(map_projection(4,50,100, projection_list = projection_list))
            )
          )

def update_remove_donor():
    while True:
        try:
            response = input(update_prompt)
            if sub_update_remove_dict[response]() == 'quit':
                print("\nYou have chosen to leave this submenu.")
                break
        except KeyError:
            print("\nThat is not a valid selection. Please choose 1, 2, or 3.")

def send_thank_you():
    while True:
        try:
            response = input(thank_you_prompt)
            if sub_choice_dict[response]() == 'quit':
                print("\nYou have chosen to leave this submenu.")
                break
        except KeyError:
            print("\nThat is not a valid selection. Please choose 1, 2, or 3.")

def send_letters():
    print("\nYou have chosen to send letters to everyone.")
    total_letters_sent = send_letters_per_donor()
    print(f"\nA total of {total_letters_sent} letters have been successfully sent to our donors.")
    print("A copy of those letters are now saved in your current directory.")

def send_letters_per_donor():
    NAME = 0
    SUM = 1

    total_letters = 0
    letter_list = dh.letter_query()
    for each_donor in letter_list:
        donor = each_donor[NAME].title()
        #Name formatting for one word names like 'Cher' vs normal full names
        first_last = donor.split(" ")
        if len(first_last) == 1:
            first = first_last[0]
            last = ""
        else:
            first = first_last[0]
            last = first_last[1]
        total_letters += send_email(donor, each_donor[SUM], "{}_{}_{}.txt".format(first, last, date.today().isoformat()))
    return total_letters

def quit(donor=0):
    return 'quit'

def print_list():
    names = dh.get_list()
    strformat = "\nWe have {} current donors: " + ", ".join(["{}"]
                * len(names))
    print(strformat.format(len(names), *names))

def validate_add_donor(name):
    while True:
        try:
            yesno = input(yes_no_prompt)
            if add_donor_dict[yesno](name)  == 'quit':
                return False
            else:
                print("Thank you, we will add them to our system")
                dh.add_donor(name)
                return True
        except KeyError:
            print("\nThat is not a valid selection. Please choose 1 or 2.")

def update_donation():
    try:
        name = input("\nPlease enter the full name of the donor whose donation you \
would like to update >> ").lower()
        if not dh.is_current_donor(name):
            print("\n{} is not a current donor, unable to make adjustment.\n".format(
                    name.title()))
            return
        else:
            print("\n{} is indeed a current donor.".format(name.title()))
            print("\nPlease enter the donation amount we will be adjusting below.")
            old_donation = validate_update_donation()
            if not dh.is_current_donation(name.lower(), old_donation):
                print("${} is not an existing donation for {}, unable to make adjustment".format(
                        old_donation, name.title()))
                return
            else:
                print("\nPlease enter the new donation amount below.")
                new_donation = validate_update_donation()
                dh.update_donation(name, old_donation, new_donation)
    except Exception as e:
        logger.info(e)
    else:
        print("\n All of {}'s donations in the amount of ${} succesfully updated to ${}.".format(
                name.title(), old_donation, new_donation))

def  validate_update_donation():
    while True:
        try:
            donation = input("What is the amount of the donation? >> ")
            num = float(donation)
            if num < 0:
                raise ValueError
        except ValueError:
            print("\nERROR: Invalid donation amount entered. Please enter valid number.")
        else:
            return num


def validate_remove_donor(name):
    while True:
        try:
            yesno = input(yes_no_prompt)
            if remove_donor_dict[yesno](name)  == 'quit':
                return False
            else:
                print("Alright, we will remove them from our system.")
                dh.remove_donor(name)
                return True
        except KeyError:
            print("\nThat is not a valid selection. Please choose 1 or 2.")

def remove_donor():
    try:
        name = input("\nPlease enter the full name of the donor you would \
like to remove >> ").lower()
        if not dh.is_current_donor(name):
            print("\n{} is not a current donor, unable to remove.\n".format(name.title()))
            return
        else:
            print("\n{} is indeed a current donor.".format(name.title()))
            print("Are you sure you would like to remove them from the system?")
            if not validate_remove_donor(name):
                return
    except Exception as e:
        logger.info(e)
    else:
        print("\n That donor and all donation instances have successfully been removed.")
        print_list()

def thank_a_donor():
    try:
        name = input("\nPlease enter the full name of the donor you would \
like to thank >> ").lower()
        if not dh.is_current_donor(name):
            print("\n{} is not a current donor, would you like to add \
them as a new donor?".format(name.title()))
            #ask_yes_no returns False if no
            if not validate_add_donor(name):
                return
        else:
            print("\n{} is a current donor, we will update their donations."
                  .format(name.title()))
        donation = validate_donation()
        dh.add_donation(donation, name)
        print("The email you are sending is as follows:")
        print(send_email(name.title(), donation))
        print("You have successfully sent a Thank You to {}.".format(name.title()))
    except Exception as e:
        logger.info(e)

def validate_donation():
    while True:
        try:
            donation = input("How much money did they donate? (type 100 for $100) >> ")
            num = float(donation)
            if num < 0:
                raise ValueError
        except ValueError:
            print("\nERROR: Invalid donation amount entered. Please enter valid number.")
        else:
            return num

#modified to either print to screen or disk
def send_email(donor, amount, dest = 0):
    fstring =f'''
    Dear {donor},

    We would like to thank you for your generous donation
    of ${amount:.2f}. It will be put to great use!

    Thank you!
    <3 The MailRoom
    '''
    if not dest:
        return fstring
    else:
        with open(dest, 'w') as outfile:
            outfile.write(fstring)
        return 1


def create_report():
    NAME = 0
    SUM = 1
    COUNT = 2

    print("\nYou have chosen to Create a Report.")
    report_list = dh.report_query()
    report = '''
Donor Name                | Total Given | Num Gifts | Average Gift
------------------------------------------------------------------'''
    strformat = '\n{:<26}${:>13.2f}{:^12}${:>13.2f}'
    for donor in report_list:
        donation_average = donor[SUM]/donor[COUNT]
        report +=  strformat.format(donor[NAME].title(), donor[SUM],
                                    donor[COUNT], donation_average)
    return report

def print_report():
    print(create_report())

def check_if_database():
    if not os.path.isfile("mailroom.db"):
        first_run()

#Main Menu options for user
main_choice_dict = {
    "1": send_thank_you,
    "2": print_report,
    "3": send_letters,
    "4": projections,
    "5": update_remove_donor,
    "6": quit
}

#Send Thank You Sub Menu options for user
sub_choice_dict = {
    "1": print_list,
    "2": thank_a_donor,
    "3": quit
}

#Update Remove Donor submenu
sub_update_remove_dict = {
    "1": update_donation,
    "2": remove_donor,
    "3": quit
}

#dict for adding donor response
add_donor_dict = {
    "1": dh.add_donor,
    "2": quit
}

remove_donor_dict = {
    "1": dh.remove_donor,
    "2": quit
}

#Main menu to prompt user
def prompt_user():
    check_if_database()
    while True:
        try:
            response = input(main_prompt)
            if main_choice_dict[response]() == 'quit':
                print("\nYou have chosen to quit. Have a good day!")
                break
        except KeyError:
            print("\nThat is not a valid selection. Please choose option 1 - 6.")
##########################################################

if __name__ == '__main__':
    prompt_user()



