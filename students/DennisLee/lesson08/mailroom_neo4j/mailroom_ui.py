"""
This module implements the mailroom user interface.
"""

#!/usr/bin/env python3

import os
import mailroom_oo_neo4j as mailroom_oo

def stripped_input(prompt):
    """Return user input, with leading and trailing spaces removed."""
    return input(prompt).strip()

class DonorUI():
    """
    This class contains the donor mailroom UI functionality.
    """
    def __init__(self, coll):
        if isinstance(coll, mailroom_oo.DonorCollection):
            self.collection = coll
        else:
            raise TypeError("Must initialize with a DonorCollection object.")

    def manage_donors(self):
        """
        Display the menu of choices for donor management.

        :return:  None.
        """
        # create a dict of menu items/ menu text/ menu caller functions
        choices = {
            '1': {'option': 'Send a thank you', 'function': self.send_thank_you},
            '2': {'option': 'Create gift report', 'function': self.collection.create_gift_report},
            '3': {'option': 'Send all letters', 'function': self.send_all_letters},
            '4': {'option': 'Add donor', 'function': self.add_donor},
            '5': {'option': 'Update donor', 'function': self.update_donor_info},
            '6': {'option': 'Delete donor', 'function': self.delete_donor_and_donations},
            '7': {'option': 'Delete all data', 'function': self.collection.delete_data},
            'Z': {'option': 'Quit', 'function': self.exit_screen}
        }

        while True:  # Print the menu list (with numbered choices)
            print("\nMENU:")
            for key, value in choices.items():
                print(key, value['option'])
            response = stripped_input("Type a menu selection number: ")
            self.call_menu_function(
                choices, response,
                self.respond_to_bad_main_menu_choice, bad_choice=response)
            if response == 'Z':  # Exit if "Quit" is chosen
                return

    def call_menu_function(
            self, choice_dict, choice, unfound_key_handler, **kwargs):
        """
        Call a menu function with a dict.

        :choice_dict:  Dict containing the `choice` string, with the dict
                       value being a another dict that contains a 'function'
                       key whose value is the function to call for `choice`.

        :choice:  A string that may or may not be a key in the choice_dict
                  dictionary.

        :unfound_key_handler:  The function to call if the specified choice
                               is not a key in the dictionary.

        :kwargs:  Additional keyword arguments to pass to the unfound key
                  handler.

        :return:  `True` if a menu function was successfully called;
                  `False` otherwise (which also can be the desired result).
        """
        try:  # Get the selection number and call helper function
            choice_dict[choice]['function']()
        except KeyError:
            unfound_key_handler(**kwargs)
            return False
        else:
            return True

    def respond_to_bad_main_menu_choice(self, bad_choice):
        """
        Show error message if the user's main menu choice is invalid.

        :bad_choice:  The menu choice string as entered by the user.

        :return:  None.
        """
        print(f"\n'{bad_choice}' is an invalid response.")

    def exit_screen(self):
        """
        Simply print an exit message.

        :return:  None.
        """
        print("\nExiting.\n")
        return

    def send_thank_you(self):
        """
        Add a new donation for an existing donor, and send a thank-you
        letter.

        :return:  None.
        """
        name = self.choose_donor()
        donation = stripped_input(
            "\nType the amount to give (or leave blank to quit): "
        )
        when = stripped_input(
            "\nType the date of the donation, in YYYY-MM-DD format: "
        )
        try:
            self.collection.add_new_amount(name, donation, when)
            print(f"\nDonor {name}'s gift of {donation} "
                  f"on {when} successfully added.\n")
            print(self.collection.form_letter(name, when))
        except ValueError as verr:
            print(verr)

    def send_all_letters(self):
        """
        Create all of the donor thank-you letters.

        :return:  None.
        """
        # Ask for the directory to save the letters to
        print('\nThe current directory is %s' % os.getcwd())
        new_dir = stripped_input(
            '\nType the directory to save the letters in'
            ' (blank entry defaults to the current directory): '
        )
        try:
            self.collection.save_letters(new_dir)
        except FileNotFoundError:
            print(f"Can't open or create folder '{new_dir}' - exiting "
                  "without creating the thank-you letters.")
        except PermissionError:
            print(f"Not allowed to write to '{new_dir}'.")
        except OSError:
            print(f"Specified folder '{new_dir}' is not valid.")

    def add_donor(self):
        """
        Add a new donor name to the donor list.

        :return:  None.
        """
        name = stripped_input("Enter a new donor name: ")
        if self.collection.get_single_donor_info(name):
            print(f"Donor {name} already exists - exiting.")
        else:
            ssn = stripped_input("Enter social security number: ")
            if not ssn:
                ssn = 'N/A'
            print(f"\nAdding donor '{name}' with SS #{ssn}.\n")
            self.collection.add_or_update_donor(name, ssn)

    def update_donor_info(self):
        """
        Update a donor's information. For now, the only information
        to update is the donor's hometown.

        :return:  None.
        """
        donor_name = self.choose_donor()
        if donor_name == '':
            print("\nExiting without updating a donor.\n")
        else:
            info = self.collection.get_donor_info(donor_name)
            print(f"\nDonor {info['person_name']}, SS # {info['ssn']}.\n")
            ssn = stripped_input(
                "Specify a new social security number (or leave blank "
                "to exit). Type N/A if the donor SS number is unknown. "
            )
            if ssn:
                self.collection.add_or_update_donor(donor_name, ssn)

    def delete_donor_and_donations(self):
        """
        Delete a donor from the Person table and their gifts from the
        Donations table.

        :return:  None.
        """
        donor_name = self.choose_donor()
        if donor_name == '':
            print("\nExiting without deleting a donor.\n")
        else:
            self.collection.delete_donor_data(donor_name)
            print(f"\nDonor {donor_name} has been deleted!\n")

    def choose_donor(self):
        """
        Prompt for the user to select a donor from the full donor list.

        :return:  The name of an existing donor, or an empty string.
        """
        response = ''
        donor_list = self.collection.get_donor_list()
        if not donor_list:
            print("\nNo donors to list.\n")
        else:
            print("\nLIST OF DONORS:")
            for key, value in donor_list.items():
                print(f"\t{key}: Social Security # {value}")
            print("\n")
            while response not in donor_list:
                response = stripped_input(
                    "Type an existing donor name (or leave blank to exit): "
                )
                if response == '':
                    break
        return response


if __name__ == '__main__':
    # Initial donor list w/possible keys (email address, phone number,
    # social security number, and birthdate) - will use SS # only though
    DONOR_SPECS = [
        {
            'person_name': 'Red Herring',
            'email': 'RedH@gmail.com',
            'phone': '468-135-0987',
            'ssn': '372-98-0038',
            'birthdate': '1952-06-28'
        },
        {
            'person_name': 'Tight Wad',
            'email': 'TWad@yahoo.com',
            'phone': '800-382-3864',
            'ssn': '016-53-3487',
            'birthdate': '1985-11-30'
        },
        {
            'person_name': 'Papa Smurf',
            'email': 'PapaSmurf@live.com',
            'phone': '369-486-0368',
            'ssn': '833-46-3487',
            'birthdate': '1976-12-02'
        },
        {
            'person_name': 'Cheap Skate',
            'email': 'NoCash@gandi.net',
            'phone': '245-748-4392',
            'ssn': '467-43-1793',
            'birthdate': '1946-02-27'
        },
        {
            'person_name': 'Pat Panda',
            'email': 'PatPan@excite.com',
            'phone': '682-843-4873',
            'ssn': '324-32-2345',
            'birthdate': '1966-07-08'
        },
        {
            'person_name': 'Karl-Heinz Berthold',
            'email': 'KHB@lufthansa.com',
            'phone': '296-348-9483',
            'ssn': '248-45-4893',
            'birthdate': '1964-02-10'
        },
        {
            'person_name': 'Mama Murphy',
            'email': 'MamaM@MamaMurphy.org',
            'phone': '748-938-8437',
            'ssn': '238-09-9816',
            'birthdate': '1964-05-02'
        },
        {
            'person_name': 'Daphne Dastardly',
            'email': 'Daphne@Dastardly.net',
            'phone': '554-382-1010',
            'ssn': '073-53-4832',
            'birthdate': '1990-06-30'
        }
    ]

    # Initial donation amounts, with donor name and date of gift
    DONOR_GIFTS = [
        {'donor_name': 'Papa Smurf', 'donation_amount': 48, 'donation_date': '2018-06-29'},
        {'donor_name': 'Papa Smurf', 'donation_amount': 57.86, 'donation_date': '2017-02-01'},
        {'donor_name': 'Daphne Dastardly', 'donation_amount': 82, 'donation_date': '2017-09-22'},
        {'donor_name': 'Papa Smurf', 'donation_amount': 210.64, 'donation_date': '2015-09-15'},
        {'donor_name': 'Papa Smurf', 'donation_amount': 351.22, 'donation_date': '2018-01-01'},
        {'donor_name': 'Mama Murphy', 'donation_amount': 600, 'donation_date': '2017-09-26'},
        {'donor_name': 'Mama Murphy', 'donation_amount': 785.2, 'donation_date': '2018-03-03'},
        {'donor_name': 'Papa Smurf', 'donation_amount': 1000, 'donation_date': '2016-11-12'},
        {'donor_name': 'Bill Dill', 'donation_amount': 2000, 'donation_date': '2015-05-27'},  # Will be rejected - not in donor list
        {'donor_name': 'Red Herring', 'donation_amount': 2500, 'donation_date': '2018-06-20'},
        {'donor_name': 'Papa Smurf', 'donation_amount': 2804.83, 'donation_date': '2017-08-15'},
        {'donor_name': 'Karl-Heinz Berthold', 'donation_amount': 3545.2, 'donation_date': '2018-01-31'},
        {'donor_name': 'Mama Murphy', 'donation_amount': 8500.3, 'donation_date': '2014-12-12'},
        {'donor_name': 'Karl-Heinz Berthold', 'donation_amount': 10579.31, 'donation_date': '2018-03-31'},
        {'donor_name': 'Mama Murphy', 'donation_amount': 12054.33, 'donation_date': '2017-02-28'},
        {'donor_name': 'Pat Panda', 'donation_amount': 14920.5, 'donation_date': '2018-03-12'},
        {'donor_name': 'Red Herring', 'donation_amount': 15000, 'donation_date': '2017-12-31'},
        {'donor_name': 'Red Herring', 'donation_amount': 31126.37, 'donation_date': '2017-08-31'},
        {'donor_name': 'Pat Panda', 'donation_amount': 35570.53, 'donation_date': '2016-10-28'},
        {'donor_name': 'Pat Panda', 'donation_amount': 55324.4, 'donation_date': '2014-05-25'},
        {'donor_name': 'Red Herring', 'donation_amount': 65820.5, 'donation_date': '2017-05-03'},
        {'donor_name': 'Mama Murphy', 'donation_amount': 156316.99, 'donation_date': '2013-07-30'}
    ]

    DONOR_COL = mailroom_oo.DonorCollection()
    DONOR_COL.bulk_insert_donors(DONOR_SPECS)
    DONOR_COL.bulk_insert_gifts(DONOR_GIFTS)

    DUI = DonorUI(DONOR_COL)
    DUI.manage_donors()
