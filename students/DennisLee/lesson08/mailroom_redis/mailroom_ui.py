"""
This module implements the mailroom user interface.
"""

#!/usr/bin/env python3

import os
# import mailroom_model as mdl
import mailroom_oo_redis as mailroom_oo

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
            for k, v in choices.items():
                print(k, v['option'])
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
        donation = input("\nType the amount to give (or leave blank to quit): ")
        when = stripped_input(
            "\nType the date of the donation, in YYYY-MM-DD format: "
        )
        try:
            self.collection.add_new_amount(name, donation, when)
            print(f"\nDonor {name}'s gift of {donation} on {when} successfully added.\n")
            print(self.collection.form_letter(name))
        except ValueError as ve:
            print(ve)

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
        if self.collection.get_donor_info(name):
            print(f"Donor {name} already exists - exiting.")
        else:
            phone_num = stripped_input("Enter phone number: ")
            if not phone_num:
                phone_num = 'N/A'
            print(f"\nAdding donor {name} with phone #{phone_num}.\n")
            self.collection.add_or_update_donor(name, phone_num)

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
            print(f"\nDonor {info[0]}, phone # {info[1]}.\n")
            phone_num = stripped_input(
                "Specify a new phone number (or leave blank to exit). " +
                "Type N/A if the donor phone number is unknown. "
            )
            if phone_num:
                self.collection.add_or_update_donor(donor_name, phone_num)

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
        Prompt for the user to type a donor from the full donor list.

        :return:  The name of an existing donor, or an empty string.
        """
        response = ''
        donor_list = self.collection.get_donor_list()
        if not donor_list:
            print("\nNo donors to list.\n")
        else:
            print("\nLIST OF DONORS:")
            for k, v in donor_list.items():
                print(f"\t{k}: phone # {v}")
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
    # social security number, and birthdate) - will use phone # only tho
    DS_EMAIL, DS_PHONE, DS_SSN, DS_BIRTHDATE = 0, 1, 2, 3
    DONOR_SPECS = {
        'Red Herring': ('RedH@gmail.com', '468-135-0987', '372-98-0038', '1952-06-28'),
        'Tight Wad': ('TWad@yahoo.com', '800-382-3864', '016-53-3487', '1985-11-30'),
        'Papa Smurf': ('PapaSmurf@live.com', '369-486-0368', '833-46-3487', '1976-12-02'),
        'Cheap Skate': ('NoCash@gandi.net', '245-748-4392', '467-43-1793', '1946-02-27'),
        'Pat Panda': ('PatPan@excite.com', '682-843-4873', '324-32-2345', '1966-07-08'),
        'Karl-Heinz Berthold': ('KHB@lufthansa.com', '296-348-9483', '248-45-4893', '23417'),
        'Mama Murphy': ('MamaM@MamaMurphy.org', '748-938-8437', '238-09-9816', '23499'),
        'Daphne Dastardly': ('Daphne@Dastardly.net', '554-382-1010', '073-53-4832', '43692')
    }

    # Initial donation amounts, with donor name and date of gift
    DG_NAME, DG_AMOUNT, DG_DATE = 0, 1, 2
    DONOR_GIFTS = (
        ('Papa Smurf', 48, '2018-06-29'),
        ('Papa Smurf', 57.86, '2017-02-01'),
        ('Daphne Dastardly', 82, '2017-09-22'),
        ('Papa Smurf', 210.64, '2015-09-15'),
        ('Papa Smurf', 351.22, '2018-01-01'),
        ('Mama Murphy', 600, '2017-09-26'),
        ('Mama Murphy', 785.2, '2018-03-03'),
        ('Papa Smurf', 1000, '2016-11-12'),
        ('Bill Dill', 2000, '2015-05-27'),  # Will be rejected -donor not in DB
        ('Red Herring', 2500, '2018-06-20'),
        ('Papa Smurf', 2804.83, '2017-08-15'),
        ('Karl-Heinz Berthold', 3545.2, '2018-01-31'),
        ('Mama Murphy', 8500.3, '2014-12-12'),
        ('Karl-Heinz Berthold', 10579.31, '2018-03-31'),
        ('Mama Murphy', 12054.33, '2017-02-28'),
        ('Pat Panda', 14920.5, '2018-03-12'),
        ('Red Herring', 15000, '2017-12-31'),
        ('Red Herring', 31126.37, '2017-08-31'),
        ('Pat Panda', 35570.53, '2016-10-28'),
        ('Pat Panda', 55324.4, '2014-05-25'),
        ('Red Herring', 65820.5, '2017-05-03'),
        ('Mama Murphy', 156316.99, '2013-07-30')
    )

    DONOR_COL = mailroom_oo.DonorCollection()
    for donor_key, donor_value in DONOR_SPECS.items():
        DONOR_COL.add_or_update_donor(donor_key, donor_value[DS_PHONE])

    for donor in DONOR_GIFTS:
        DONOR_COL.add_new_amount(
            donor[DG_NAME], donor[DG_AMOUNT], donor[DG_DATE]
        )

    DUI = DonorUI(DONOR_COL)
    DUI.manage_donors()
