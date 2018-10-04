"""
This module implements the mailroom user interface.
"""

#!/usr/bin/env python3

import os
# import mailroom_model as mdl
import mailroom_oo

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
            response = input("Type a menu selection number: ").strip()
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
        Add new donations for new or existing donors, and send a thank-you
        letter.

        :return:  None.
        """
        alt_choices = {  # Dict of functions to show donor list or to quit
            '': {'function': self.exit_screen},
            'quit': {'function': self.exit_screen},
            'list': {'function': self.collection.choose_donor}
        }
        # Get the donor name, show all donors, or quit
        response = input("\nType full donor name "
                         "(or 'list' to show all donors, or 'quit'): ").strip()

        self.call_menu_function(alt_choices, response,
                                self.get_donation_amount, donor=response)
        if response == 'list':
            self.send_thank_you()  # Still want to get a donor to thank

    def get_donation_amount(self, person):
        """
        Ask user for a donation amount from the specified donor.

        :person:  The name of the person to make the donation.

        :return:  None.
        """
        donation_choices = {  # Dict of functions if user wants to quit
            '': {'function': self.exit_screen},
            'quit': {'function': self.exit_screen}
        }
        donation = input(f"Type amount to donate (or type 'quit'): "
                        ).strip().lower()
        try:
            self.call_menu_function(
                donation_choices, donation,
                self.collection.add_new_amount, name=person, amount=donation)
        except ValueError:
            print(f"'{donation}' is not a valid donation amount.")

    def send_all_letters(self):
        """
        Create all of the donor thank-you letters.

        :return:  None.
        """
        # Ask for the directory to save the letters to
        print('\nThe current directory is %s' % os.getcwd())
        new_dir = input('\nType the directory to save the letters in'
                        ' (blank entry defaults to the current directory): '
                       ).strip()
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
        name = input("Enter a new donor name: ").strip()
        if self.collection.get_donor_info(name):
            print(f"Donor {name} already exists - exiting.")
        else:
            town = input("Enter hometown (leave blank if unknown): ").strip()
            if not town:
                town = 'N/A'
            print(f"\nAdding donor {name} with hometown {town}.\n")
            self.collection.add_or_update_donor(name, town)

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
            print(f"\nDonor {info['donor']} lives in {info['hometown']}.\n")
            new_town = input(
                "Specify a new hometown (or leave blank to exit). " +
                "Type N/A if the donor residence is unknown. "
            ).strip()
            if new_town:
                self.collection.update_donor(donor_name, new_town)

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

        :return:  None.
        """
        response = ''
        donor_list = self.collection.get_donor_list()
        if not donor_list:
            print("\nNo donors to list.\n")
        else:
            print("\nLIST OF DONORS:")
            for k, v in donor_list.items():
                print(f"\t{k} (lives in {v})")
            print("\n")
            while response not in donor_list:
                response = input(
                    "Type an existing donor name (or leave blank to exit): "
                ).strip()
                if response == '':
                    break
            return response.strip()


if __name__ == '__main__':
    # Initial donor list and the amounts they have donated
    DS_NAME, DS_TOWN = 0, 1
    donor_specs = (
        ('Red Herring', 'Amarillo'),
        ('Tight Wad', 'Chicago'),
        ('Papa Smurf', 'Zurich'),
        ('Cheap Skate', 'Amarillo'),
        ('Pat Panda', 'Chicago'),
        ('Karl-Heinz Berthold', 'Bremen'),
        ('Mama Murphy', 'Chicago'),
        ('Daphne Dastardly', 'Gotham')
    )

    DG_NAME, DG_AMOUNT, DG_DATE = 0, 1, 2
    donor_gifts = (
        ('Papa Smurf', 48, '2018-06-29'),
        ('Papa Smurf', 57.86, '2017-02-01'),
        ('Daphne Dastardly', 82, '2017-09-22'),
        ('Papa Smurf', 210.64, '2015-09-15'),
        ('Papa Smurf', 351.22, '2018-01-01'),
        ('Mama Murphy', 600, '2017-09-26'),
        ('Mama Murphy', 785.2, '2018-03-03'),
        ('Papa Smurf', 1000, '2016-11-12'),
        ('Bill Dill', 2000, '2015-05-27'),
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

    donor_col = mailroom_oo.DonorCollection()
    for donor in donor_specs:
        donor_col.add_or_update_donor(donor[DS_NAME], donor[DS_TOWN])

    for donor in donor_gifts:
        donor_col.add_new_amount(
            donor[DG_NAME], donor[DG_AMOUNT], donor[DG_DATE]
        )

    dui = DonorUI(donor_col)
    dui.manage_donors()
