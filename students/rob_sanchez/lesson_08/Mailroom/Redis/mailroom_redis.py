#!/usr/bin/env python3
import sys
import re
import json
from donor_class import *
import os


# New instance of the MyDonation class
donations_list = MyDonations()


def main():
    """
        Displays the main menu selection options
    """
    # Menu options
    options = {1: send_thank_you,
               2: create_report,
               3: send_letters,
               4: challenge,
               5: update_donor,
               6: update_donation,
               7: delete_donor,
               8: delete_donation,
               9: load_initial_donors,
               10: validate_donor,
               0: sys.exit}
    prompt = "\nChoose an action:\n"
    menu_sel = ("\n1 - Send a Thank You\n2 - Create a Report\n"
                "3 - Send letters to everyone\n4 - Projections\n\n"
                "5 - Update Donor\n6 - Update Donation\n\n"
                "7 - Delete Donor\n8 - Delete Donation\n\n"
                "9 - Load Initial Donors\n\n*10 - Donor Validation Lookup\n\n"
                "0 - Quit\n\n")

    # User selection
    while True:
        try:
            user_selection = input(prompt + menu_sel)
            options.get(int(user_selection))()
        except ValueError:
            print("\nPlease select a numeric value...")
        # except TypeError as e:
        #     print(e)
            # print("\nOption {} is invalid. Try again...".format(user_selection))


def send_thank_you():
    """
        Sends a thank you email to the selected donor
    """

    # Get name of donor
    donor_name = name_prompt()

    # Display list of donors when user types "list"
    while donor_name.lower() == "list":
        donations_list.get_formatted_list_of_donors()
        donor_name = name_prompt()

    # Get donation amount
    amt_input = donation_prompt()

    donations_list.add_donation(donor_name, float(amt_input))

    print(send_email(donations_list.get_last_donation(donor_name)))


def create_report():
    """
        Displays a summary report of the current list of donations
    """
    donations_list.get_summary


def send_letters():
    """
        reates a thank you letter for each donor as a
        text document
    """

    for value in donations_list.get_list_of_donors():
        name = str(value)

        if not os.path.exists('letters/'):
            os.makedirs('letters/')

        with open("letters/"+name+".txt", 'w') as f:
            f.write(create_letter(donations_list.get_donor_summary(name)))
        print("\nLetter to {} has been sent...".format(name))


def challenge():
    """
        Challenges a donor's current donations for a given range
        and with a given multiplier value
    """
    while True:
        try:
            donor_name = name_prompt()

            # Display list of donors when user types "list"
            while donor_name.lower() == "list":
                donations_list.get_formatted_list_of_donors()
                donor_name = name_prompt()

            # Display current list of donations
            donations_list.get_formatted_list_of_donations(donor_name)

            min = min_prompt()
            max = max_prompt()
            multiplier = multiplier_prompt()
            print(donations_list.challenge(donor_name, factor=multiplier, min=min, max=max))
            break
        except ValueError:
            print("\n>> Please enter a valid donor name <<")
        except KeyError:
            print("\n>> Donor not found <<")


def update_donor():
    """
        Updates a donor's current name
    """
    while True:
        try:
            # Get name of donor to be updated
            donor_name = name_prompt()

            # Display list of donors when user types "list"
            while donor_name.lower() == "list":
                donations_list.get_formatted_list_of_donors()
                donor_name = name_prompt()

            # Get donor's new name
            new_name = new_name_prompt()

            donations_list.update_donor(donor_name, new_name)
            break
        except ValueError:
            print("\n>> Donor not found <<")


def update_donation():
    """
        Updates a donor's donation
    """

    while True:
        try:
            # Get name of donor to be deleted
            donor_name = name_prompt()

            # Display list of donors when the user types "list"
            while donor_name.lower() == "list":
                donations_list.get_formatted_list_of_donors()
                donor_name = name_prompt()

            # Display current list of donations
            donations_list.get_formatted_list_of_donations(donor_name)

            donation = donation_prompt()
            new_donation = new_donation_prompt()

            donations_list.update_donation(donor_name, donation, new_donation)

            break
        except ValueError:
            print("\n>> Donor not found <<")
        except DonationError:
            print("\n>> Donation not found <<")


def delete_donor():
    """
        Deletes the specified donor and donations from the database
    """
    while True:
        try:
            # Get name of donor to be deleted
            donor_name = name_prompt()

            # Display list of donors when user types "list"
            while donor_name.lower() == "list":
                donations_list.get_formatted_list_of_donors()
                donor_name = name_prompt()

            donations_list.delete_donor(donor_name)
            break
        except ValueError:
            print("\n>> Donor not found <<")


def delete_donation():
    """
        Deletes the specified donor's donation
    """
    donor_name = ""
    donation = 0

    while True:
        try:
            # Get name of donor to be deleted
            donor_name = name_prompt()

            # Display list of donors when the user types "list"
            while donor_name.lower() == "list":
                donations_list.get_formatted_list_of_donors()
                donor_name = name_prompt()

            # Display current list of donations
            donations_list.get_formatted_list_of_donations(donor_name)

            donation = donation_prompt()

            donations_list.delete_donation(donor_name, donation)
            break
        except ValueError:
            print("\n>> Donor not found <<")
        except DonationError:
            print("\n>> Donation not found <<")


def load_initial_donors():
    """
        Loads the initial list of donors and donations
    """
    donations_list.load_initial_donors()


def validate_donor():
    """
        Gives the user the ability validate a donor's information
    """
    donations_list.update_cache()
    val_value = ''

    # Get name of donor to validate
    donor_name = name_prompt()

    # Display list of donors when user types "list"
    while donor_name.lower() == "list":
        donations_list.get_formatted_list_of_donors()
        donor_name = name_prompt()

    while val_value.lower() != "done":
        # Get name of donor to validate
        val_value = lookup_prompt()

        donations_list.donor_lookup(donor_name, val_value)
        print("\n--Type 'done' to return to main menu.\n")


####
# Helper methods:
####
def name_prompt():
    """
        Prompts the user for the name of donor to send thank you email
    """
    while True:
        try:
            name = input("\nPlease enter the Donor's full name:\n" +
                         "(Type 'list' to display a list of current donors): ").strip()
            if re.match("^[A-Za-z ,]*$", name) and name:
                return name
                break
            else:
                print("\n>> Please enter a valid name <<")
        except ValueError:
            print("\n>> Please enter a valid name <<")


def new_name_prompt():
    """
        Prompts the user for the donor's updated name
    """
    while True:
        try:
            name = input("\nPlease enter the Donor's new name:\n").strip()
            if re.match("^[A-Za-z ,]*$", name) and name:
                return name
                break
            else:
                print("\n>> Please enter a valid name <<")
        except ValueError:
            print("\n>> Please enter a valid name <<")


def donation_prompt():
    """
        Prompts the user for a donation amount
    """
    while True:
        try:
            amount = re.sub("[, ]", "", input("\nDonation amount:\n$"))
            return round(float(amount), 2)
            break
        except ValueError:
            print("\n>> Please enter a valid donation amount <<")


def new_donation_prompt():
    """
        Prompts the user for the updated donatino amount
    """
    while True:
        try:
            amount = re.sub("[, ]", "", input("\nNew donation amount:\n$"))
            return round(float(amount), 2)
            break
        except ValueError:
            print("\n>> Please enter a valid donation amount <<")


def multiplier_prompt():
    """
        Prompts the user for the donation multiplier factor
    """
    while True:
        try:
            multiplier = re.sub("[, ]", "", input("\nMultiply donations by: "))
            return int(multiplier)
            break
        except ValueError:
            print("\n>> Please enter a valid multiplier <<")


def min_prompt():
    """
        Prompts the user for the minimum projection donation
    """
    while True:
        try:
            min = re.sub("[, ]", "", input("\nMin donation (Press enter for default value): "))
            return round(float(0), 2) if not min else round(float(min), 2)
            break
        except ValueError:
            print("\n>> Please enter a valid minimum value <<")


def max_prompt():
    """
        Prompts the user for the maximum projection donation
    """
    while True:
        try:
            max = re.sub("[, ]", "", input("\nMax donation (Press enter for default value): "))
            return round(float(9999999), 2) if not max else round(float(max), 2)
            break
        except ValueError:
            print("\n>> Please enter a valid maximum value <<")


def lookup_prompt():
    """
        Prompts the user for a validation value
    """
    list_of_values = ['phone', 'email', 'zip', 'last donation', 'last donation date',
                      'all', 'done']

    while True:
        try:
            value = (input("\nPlease enter a lookup value:\n" +
                           "(phone, email, zip, last donation, last donation date, all): ")
                     .strip().lower())
            if re.match("^[A-Za-z ,]*$", value) and value and value in list_of_values:
                return value.replace(' ', '_')
                break
            else:
                print("\n>> Please enter a valid lookup value <<")
        except ValueError:
            print("\n>> Please enter a valid lookup value <<")


def send_email(new_donor):
    """
        Formats the email for newly added donors
    """
    body = ("\nDear {donor_name},\n\n"
            "I would like to personally thank you for your generours donation "
            "of ${amount} to our charity organization.\nYour support allows us"
            " to continue supporting more individuals in need of our services."
            "\n\nSincerely,\nCharity Inc.\n").format(**new_donor)
    return body


def create_letter(donations):
    """
        Formats the letter for the current list of donors
    """
    body = ("\nDear {donor_name},\n\n"
            "I would like to personally thank you for your recent "
            "donation of ${last_donation} to our charity organization. "
            "You have donated a total of ${total} as of today. "
            "Your support allows us to continue supporting more individuals "
            "in need of our services."
            "\n\nSincerely,\nCharity Inc.\n").format(**donations)
    return body


if __name__ == "__main__":
    main()
