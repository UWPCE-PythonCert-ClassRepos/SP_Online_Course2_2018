"""
This module implements the mailroom user interface.
"""

#!/usr/bin/env python3

import os
import mailroom_model as mdl
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
            '2': {'option': 'Create a report', 'function': self.collection.create_report},
            '3': {'option': 'Send all letters', 'function': self.send_all_letters},
            '4': {'option': 'Quit', 'function': self.exit_screen}
        }

        while True:  # Print the menu list (with numbered choices)
            print("\nMENU:")
            for k, v in choices.items():
                print(k, v['option'])
            response = input("Type a menu selection number: ").strip()
            self.call_menu_function(
                choices, response,
                self.respond_to_bad_main_menu_choice, bad_choice=response)
            if response == '4':  # Exit if "Quit" is chosen
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
            'list': {'function': self.collection.print_donors}
        }
        # Get the donor name, show all donors, or quit
        response = input("\nType full donor name "
                         "(or 'list' to show all donors, or 'quit'): ").strip()

        self.call_menu_function(alt_choices, response,
                                self.get_donation_amount, donor=response)
        if response == 'list':
            self.send_thank_you()  # Still want to get a donor to thank

    def get_donation_amount(self, donor):
        """
        Ask user for a donation amount from the specified donor.

        :donor:  A `Donor` object for which to add a donation amount.

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
                self.collection.add, name=donor, amount=donation)
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


if __name__ == '__main__':
    # Initial donor list and the amounts they have donated
    DH_NAME, DH_TOWN, DH_AMTS = 0, 1, 2
    donor_history = (
        ('Red Herring', 'Amarillo', [65820.5, 31126.37, 15000, 2500]),
        ('Papa Smurf', 'Zurich', [210.64, 1000, 57.86, 2804.83, 351.22, 48]),
        ('Pat Panda', 'Chengdu', [55324.4, 35570.53, 14920.50]),
        ('Karl-Heinz Berthold', 'Bremen', [3545.2, 10579.31]),
        ('Mama Murphy', 'Chicago', [156316.99, 8500.3, 12054.33, 600, 785.20]),
        ('Daphne Dastardly', 'Gotham', [82])
    )

    donor_col = mailroom_oo.DonorCollection()
    for donor in donor_history:
        donor_col.add_or_update_donor(donor[DH_NAME], donor[DH_TOWN])
        for amount in donor[DH_AMTS]:
            donor_col.add_new_amount(donor[DH_NAME], amount)

    dui = DonorUI(donor_col)
    dui.manage_donors()
